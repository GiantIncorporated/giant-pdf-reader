"""
Tests for PdfCache.

Covers:
  - normal store/fetch roundtrip preserves page data exactly (including
    nested structures and unicode text extracted from PDFs)
  - a corrupted/incompatible cache entry degrades to a cache miss instead
    of raising and killing the render pipeline
  - the read=True (raw file-like / streaming) path bypasses JSON+zlib
    entirely, since it's used for binary blobs, not page data
"""
import io
import json
import zlib

import pytest
from diskcache import Cache

from pdf_reader.core.caches.pdf_cache import PdfCache

PAGE_PAYLOAD = {
    "page_number": 3,
    "text": "Hello, world — café résumé 你好",
    "words": [
        {"text": "Hello,", "bbox": [10.5, 20.0, 40.2, 30.0]},
        {"text": "world", "bbox": [42.0, 20.0, 70.1, 30.0]},
    ],
    "images": [],
    "rotation": 0,
}


@pytest.fixture
def cache(tmp_path):
    """A real diskcache.Cache backed by PdfCache, on a temp directory."""
    c = Cache(str(tmp_path), disk=PdfCache)
    yield c
    c.close()


class TestRoundtrip:
    def test_dict_roundtrips_exactly(self, cache):
        cache.set("page-3", PAGE_PAYLOAD)
        assert cache.get("page-3") == PAGE_PAYLOAD

    def test_unicode_text_preserved(self, cache):
        payload = {"text": "日本語のテスト — emoji 🎉"}
        cache.set("unicode-page", payload)
        assert cache.get("unicode-page")["text"] == payload["text"]

    def test_empty_and_falsy_values_roundtrip(self, cache):
        for key, value in [
            ("empty-dict", {}),
            ("empty-list", []),
            ("zero", 0),
            ("empty-string", ""),
        ]:
            cache.set(key, value)
            assert cache.get(key) == value

    def test_large_page_data_roundtrips(self, cache):
        # Simulates a text-heavy page; also exercises the on-disk
        # (vs. inline sqlite) storage path for larger blobs.
        big_payload = {
            "text": "word " * 50_000,
            "words": [{"text": "word", "bbox": [0, 0, 1, 1]}] * 5_000,
        }
        cache.set("big-page", big_payload)
        assert cache.get("big-page") == big_payload

    def test_missing_key_returns_default(self, cache):
        assert cache.get("does-not-exist") is None
        assert cache.get("does-not-exist", default="fallback") == "fallback"


class TestCompression:
    def test_stored_bytes_are_actually_compressed(self, cache):
        cache.set("page-3", PAGE_PAYLOAD)
        raw = cache._disk.store(PAGE_PAYLOAD, read=False)
        # store() returns (size, mode, filename, value) per diskcache's
        # Disk.store contract; for small values the compressed bytes end
        # up in `value` directly.
        _, _, _, stored_value = raw
        json_bytes = json.dumps(PAGE_PAYLOAD).encode("utf-8")
        assert bytes(stored_value) == zlib.compress(json_bytes, 1)
        assert len(bytes(stored_value)) <= len(json_bytes)


class TestCorruptionIsGracefulMiss:
    def test_fetch_with_undecompressable_bytes_raises_ioerror(self, monkeypatch):
        """
        fetch() must turn corrupt/incompatible data into an IOError —
        that's the *only* exception diskcache.Cache.get() catches and
        converts to "return default" (see Cache.get's `except IOError`
        clause). Any other exception type, including the zlib.error /
        json.JSONDecodeError this would otherwise raise, propagates
        straight up and crashes the caller.
        """
        disk = PdfCache.__new__(PdfCache)  # avoid needing a real directory
        disk._encoding = "utf-8"

        monkeypatch.setattr(
            "diskcache.Disk.fetch",
            lambda self, mode, filename, value, read: b"not valid zlib-compressed json",
        )

        with pytest.raises(IOError):
            PdfCache.fetch(disk, mode=0, filename="some.val", value=None, read=False)

    def test_corrupted_disk_entry_is_a_cache_miss_not_a_crash(self, cache, monkeypatch):
        """
        End-to-end: simulate a cache entry that got corrupted/truncated
        on disk (e.g. partial write, different compress_level in a prior
        run). Fetching it should behave like a normal cache miss so the
        caller just re-renders the page, instead of raising and taking
        down the render pipeline.
        """
        cache.set("page-3", PAGE_PAYLOAD)

        # Force the underlying Disk.fetch to return bytes that can't be
        # decompressed, simulating on-disk corruption.
        def corrupted_fetch(self, mode, filename, value, read):
            return b"\x00\x01corrupted-not-zlib"

        monkeypatch.setattr(
            "diskcache.Disk.fetch", corrupted_fetch, raising=True
        )

        # cache.get() catches IOError from the disk layer internally and
        # returns the default instead of propagating.
        assert cache.get("page-3", default="MISS") == "MISS"

    def test_corrupted_entry_logs_a_warning(self, cache, monkeypatch, caplog):
        cache.set("page-3", PAGE_PAYLOAD)

        def corrupted_fetch(self, mode, filename, value, read):
            return b"garbage"

        monkeypatch.setattr(
            "diskcache.Disk.fetch", corrupted_fetch, raising=True
        )

        with caplog.at_level("WARNING"):
            cache.get("page-3", default=None)

        assert any("PdfCache" in record.message for record in caplog.records)


class TestRawStreamPassthrough:
    def test_read_true_skips_json_and_compression_when_used_consistently(self, cache):
        """
        read=True stores a file-like stream of raw bytes (e.g. an image
        blob) untouched by JSON/zlib. diskcache stores it with the same
        on-disk mode it would use for our compressed JSON bytes (both
        are plain `bytes` under the hood), so PdfCache can only tell
        them apart via the `read` flag itself — meaning `read` must be
        passed the same way on get() as it was on set() for a given key.
        This is a real constraint on how PdfCache must be used, not
        just an implementation detail: raw streams and JSON page
        payloads must not be mixed under the same key, and callers
        fetching a raw-stream key must pass read=True to avoid a
        (harmless but wasteful) decompression attempt.
        """
        raw_bytes = b"%PDF-1.4 fake binary blob" * 1000
        stream = io.BytesIO(raw_bytes)

        cache.set("raw-blob", stream, read=True)
        handle = cache.get("raw-blob", read=True)
        assert handle.read() == raw_bytes
        handle.close()

    def test_mixing_read_flags_degrades_to_miss_rather_than_crashing(self, cache):
        """
        If a caller stores a raw stream with read=True but then fetches
        it the normal way (read=False, the default), PdfCache will try
        to zlib-decompress raw binary data that was never compressed.
        Thanks to the IOError contract above, this must surface as a
        clean cache miss — not an unhandled exception — even though it's
        a usage mistake rather than on-disk corruption.
        """
        raw_bytes = b"%PDF-1.4 fake binary blob" * 1000
        cache.set("raw-blob", io.BytesIO(raw_bytes), read=True)

        assert cache.get("raw-blob", default="MISS") == "MISS"