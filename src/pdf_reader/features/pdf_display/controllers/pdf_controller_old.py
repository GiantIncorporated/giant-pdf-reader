# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-08-16
# Description: This is the PdfController class responsible for handling PDF-related operations.

import os

from diskcache import Cache
from platformdirs import user_cache_dir

from core.utils.logging import Logger
from features.pdf_display.repository.pdf_repository import PdfRepository
from features.pdf_display.services.render_service.pdf_render_service_old import PdfRenderService
from features.pdf_display.services.render_service.pdf_storage_service import PDFStorageService
from features.pdf_display.workers.pdf_render_worker import PdfRenderWorker


class PdfController:

    def __init__(self, message_signal):
        self._signal = message_signal
        self._cache = Cache(directory=os.path.join(user_cache_dir("giantpdf", "giantinc"), "PDFCache"))

        self._pdf_repository = PdfRepository(self._cache)
        self._storage_service = PDFStorageService(pdf_repository=self._pdf_repository, signal=message_signal)
        self._render_service = PdfRenderService(pdf_repository=self._pdf_repository)
        self._pdf_worker = PdfRenderWorker(message_signal, self._render_service)

        self._file_path = None

    def fetch_page_handler(self, file_path):
        Logger.info(f"Fetching text from page, {file_path}")
        self._file_path = file_path
        self._pdf_worker.open_doc(
            target=PdfRenderService.open_doc_in_process,
            args=(self._file_path,
                  self._pdf_worker.queue_number,
                  self._pdf_worker.queue_page_info))



    def fetch_next_page_handler(self):
        is_rendered = self._storage_service.render_next_page()
        Logger.info(f"Rendered next page: {is_rendered}")
        if is_rendered:
            return
        self._pdf_worker.render_next_page()

    def fetch_prev_page_handler(self):
        is_rendered = self._storage_service.render_previous_page()
        Logger.info(f"Rendered previous page: {is_rendered}")
        if is_rendered:
            return
        self._pdf_worker.render_prev_page()
