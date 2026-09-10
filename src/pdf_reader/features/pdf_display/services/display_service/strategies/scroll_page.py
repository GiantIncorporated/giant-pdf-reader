import json
import time
from multiprocessing import cpu_count, Pool
from threading import Thread
from typing import override

from PySide6.QtCore import Signal

from core.utils.logging import Logger
from features.pdf_display.models.pdf.pdf_doc import PdfDoc
from features.pdf_display.repository.pdf_repository import PdfRepository
from features.pdf_display.services.display_service.interface.base_display import BaseDisplay
from features.pdf_display.services.render_service.pdf_service import PdfService


class ScrollPage(BaseDisplay):
    """Optimized scroll page display with parallel parsing and adaptive chunking."""

    # Adaptive chunk sizing: 1-2 pages per CPU core (tuned for emission efficiency)
    DEFAULT_CHUNK_MULTIPLIER = 1.5
    MIN_CHUNK_SIZE = 2
    MAX_CHUNK_SIZE = 25  # Prevent overly large chunks
    CHUNK_EMIT_DELAY_MS = 50  # Stagger emissions to avoid React overload

    def __init__(self, signal: Signal, pdf_repository: PdfRepository):
        self._signal = signal
        self._pdf_repository = pdf_repository
        self._chunk_size = self._calculate_chunk_size()
        Logger.debug(f"ScrollPage initialized with chunk_size={self._chunk_size}")

    @staticmethod
    def _calculate_chunk_size():
        """Dynamically calculate chunk size based on system CPU count."""
        cpu_cores = cpu_count() or 4
        size = max(
            ScrollPage.MIN_CHUNK_SIZE,
            min(
                int(cpu_cores * ScrollPage.DEFAULT_CHUNK_MULTIPLIER),
                ScrollPage.MAX_CHUNK_SIZE,
            ),
        )
        return size

    @override
    def display(self, pdf_repository: PdfRepository, current_page: int = 0):
        """Load and display pages with parallel parsing in background thread."""
        pdf_doc = pdf_repository.load_scroll_page(PdfService.state['page_count'])
        PdfService.state['current_page_num'] = current_page

        if pdf_doc is None or len(pdf_doc) == 0:
            Logger.warning("No PDF document loaded or empty page list")
            return

        # Background thread won't block UI
        thread = Thread(
            target=self._emit_pages_optimized,
            args=(pdf_doc,),
            daemon=True,
            name="PDFPageEmitter",
        )
        thread.start()

    @override
    def prev_page(self, page_number: int) -> bool:
        pass

    @override
    def next_page(self, page_number: int) -> bool:
        pass

    def _emit_pages_optimized(self, payload: list[PdfDoc]):
        """
        Emit pages in chunks with parallel parsing.
        Uses multiprocessing Pool for CPU-bound parsing work.
        """
        try:
            if not payload:
                Logger.warning("Empty payload provided to _emit_pages_optimized")
                return

            total_pages = len(payload)
            Logger.debug(
                f"Processing {total_pages} pages with chunk_size={self._chunk_size} "
                f"(total chunks: {(total_pages + self._chunk_size - 1) // self._chunk_size})"
            )

            # Use multiprocessing Pool for parallel parsing
            with Pool(processes=min(cpu_count() or 1, self._chunk_size)) as pool:
                chunk_idx = 0
                total_chunks = (total_pages + self._chunk_size - 1) // self._chunk_size

                for chunk_start in range(0, total_pages, self._chunk_size):
                    chunk_end = min(chunk_start + self._chunk_size, total_pages)
                    chunk = payload[chunk_start:chunk_end]

                    # Parallel parsing using process pool
                    start_time = time.time()
                    parsed_pages = pool.map(ScrollPage._parse_pdf_payload, chunk)
                    parse_time = time.time() - start_time

                    # Emit chunk
                    self._emit_chunk(
                        pages=parsed_pages,
                        chunk_number=chunk_idx,
                        total_chunks=total_chunks,
                        start_page=chunk[0].page_number if chunk else 0,
                        end_page=chunk[-1].page_number if chunk else 0,
                        parse_duration_ms=parse_time * 1000,
                    )

                    chunk_idx += 1

                    # Stagger emissions to prevent React event queue overload
                    if chunk_idx < total_chunks:
                        time.sleep(self.CHUNK_EMIT_DELAY_MS / 1000.0)

        except Exception as e:
            Logger.error(f"Error in _emit_pages_optimized: {e}", exc_info=True)
            self._emit_error(str(e))

    def _emit_chunk(
            self,
            pages: list[dict],
            chunk_number: int,
            total_chunks: int,
            start_page: int,
            end_page: int,
            parse_duration_ms: float = 0.0,
    ):
        """Emit a chunk of parsed pages with metadata."""

        Logger.debug(f"emit chunk {chunk_number} with {len(pages)} pages")

        payload_dict = {
            "type": "scroll_page",
            "currentPage": 0,
            "fileName": PdfRepository.file_name,
            "fileDirectory": PdfRepository.file_path,
            "page_count": PdfService.state["page_count"],
            "chunk": chunk_number,
            "total_chunks": total_chunks,
            "start_page": start_page,
            "end_page": end_page,
            "parse_duration_ms": parse_duration_ms,
            "pages": pages,
        }

        try:
            self._signal.emit(json.dumps(payload_dict))
            Logger.debug(
                f"Emitted chunk {chunk_number + 1}/{total_chunks} "
                f"({len(pages)} pages, parse: {parse_duration_ms:.1f}ms)"
            )
        except Exception as e:
            Logger.error(f"Failed to emit chunk {chunk_number}: {e}", exc_info=True)

    def _emit_error(self, error_message: str):
        """Emit an error payload to React."""
        error_dict = {
            "type": "scroll_page_error",
            "error": error_message,
        }
        try:
            self._signal.emit(json.dumps(error_dict))
        except Exception as e:
            Logger.error(f"Failed to emit error: {e}")

    @staticmethod
    def _parse_pdf_payload(pdf_page: PdfDoc) -> dict:
        """
        Parse a single PDF page object into a serializable dict.
        This is called in parallel by multiprocessing Pool workers.
        """
        try:
            return {
                "page_number": pdf_page.page_number,
                "width_pt": pdf_page.width_pt,
                "height_pt": pdf_page.height_pt,
                "canvas_width_px": pdf_page.canvas_width_px,
                "canvas_height_px": pdf_page.canvas_height_px,
                "canvas_png_b64": pdf_page.canvas_png_b64,
                "spans": pdf_page.page_spans,
            }
        except AttributeError as e:
            Logger.error(
                f"Missing attribute in PDF page {getattr(pdf_page, 'page_number', '?')}: {e}"
            )
            raise
