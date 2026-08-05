import os
import time
from multiprocessing import Process
from typing import Any, Callable

from core.services.pdf_render_service import PdfRenderService
from core.services.pdf_storage_service import PDFStorageService
from core.utils.logging import Logger


class PdfRenderWorker:
    """This class provides services for rendering PDF files."""

    def __init__(self, render_service: PdfRenderService, storage_service: PDFStorageService) -> None:
        self._process = None
        self._render_service = render_service
        self._storage_service = storage_service
        self._last_dir = ""
        self._file = None

    def render_pdf(self, page_number: int, target: Callable[..., Any], args: tuple) -> None:
        """Render the PDF file."""
        Logger.info(f"Using render service render pdf {args}")

        has_page = self._storage_service.fetch_saved_page(page_number)
        Logger.info(f"[render_pdf] has_page {has_page}")

        if has_page:
            return
        Logger.info(f"[render_pdf] has no save page {has_page}")
        (path, queue_number, queue_doc) = args
        if path:
            self._last_dir, self._file = os.path.split(path)
            if self._process:
                queue_number.put(-1)
            self._render_service.ipc_timer.timer_send.stop()
            self._render_service.current_page_number = 0
            self._render_service.page_count = 0
            self._process = Process(target=target,
                                    args=args)
            self._process.start()
            self._render_service.ipc_timer.timer_get.start(40)
            queue_number.put(0)
            self._render_service.ipc_timer.start_time = time.perf_counter()
            self._render_service.ipc_timer.timer_waiting.start(40)
