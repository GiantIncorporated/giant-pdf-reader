# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-07-26
# Description: This class provides a cache for PDF documents, allowing efficient retrieval of PDF documents based on
#              their file paths.
import json
import zlib
from diskcache import UNKNOWN, Disk

from pdf_reader.core.utils.logging import Logger


class PdfCache(Disk):
    def __init__(self, directory, compress_level=1, **kwargs):
        self._compress_level = compress_level
        self._encoding = 'utf-8'
        super().__init__(directory, **kwargs)

    def store(self, value, read, key=UNKNOWN):
        if not read:
            json_bytes = json.dumps(value).encode(self._encoding)
            value = zlib.compress(json_bytes, self._compress_level)
        return super().store(value, read, key=key)

    def fetch(self, mode, filename, value, read):
        data = super().fetch(mode, filename, value, read)
        if not read:
            try:
                data = json.loads(zlib.decompress(data).decode(self._encoding))
            except (zlib.error, UnicodeDecodeError, json.JSONDecodeError, TypeError) as exc:
                Logger.warning(
                    "PdfCache: failed to decode cached entry %s (%s); "
                    "treating as cache miss.", filename, exc
                )
                raise IOError(f"unreadable PdfCache entry: {filename}") from exc
        return data