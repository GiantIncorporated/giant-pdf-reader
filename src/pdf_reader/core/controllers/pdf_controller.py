# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-07-27
# Description: This is the PdfController class responsible for handling PDF-related operations.
import json
import os

from diskcache import Cache
from platformdirs import user_cache_dir

from core.repository.pdf_repository import PdfRepository
from core.services.pdf_render_service import PdfRenderService
from core.services.pdf_storage_service import PDFStorageService
from core.utils.logging import Logger
from core.workers.pdf_render_worker import PdfRenderWorker


class PdfController:

    def __init__(self, message_signal):
        self._cache = Cache(directory=os.path.join(user_cache_dir("giantpdf", "giantinc"), "PDFCache"))
        self._pdf_repository = PdfRepository(self._cache)
        self._storage_service = PDFStorageService(pdf_repository=self._pdf_repository, signal=message_signal)
        self._render_service = PdfRenderService(pdf_repository=self._pdf_repository, signal=message_signal)

        self._pdf_worker = PdfRenderWorker(self._render_service, self._storage_service)

    def fetch_page_handler(self, file_path, page_number):
        self._pdf_worker.render_pdf(
            page_number=page_number,
            target=PdfRenderService.open_doc_in_process,
            args=(file_path,
                  self._render_service.queue_number,
                  self._render_service.queue_page_info))
