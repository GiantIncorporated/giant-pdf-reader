# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-08-16
# Description: This is the PdfController class responsible for handling PDF-related operations.
import json
import os
from multiprocessing import cpu_count

from diskcache import Cache
from platformdirs import user_cache_dir

from core.utils.logging import Logger
from features.pdf_display.repository.pdf_repository import PdfRepository
from features.pdf_display.services.display_service.display_service import DisplayService
from features.pdf_display.services.display_service.strategies.double_page import DoublePage
from features.pdf_display.services.display_service.strategies.scroll_page import ScrollPage
from features.pdf_display.services.display_service.strategies.single_page_display import SinglePage
from features.pdf_display.services.render_service.pdf_render_service import PdfRenderService
from features.pdf_display.services.render_service.pdf_service import PdfService
from features.pdf_display.workers.pdf_render_worker import PdfRenderWorker


class PdfController:

    def __init__(self, message_signal):
        self._signal = message_signal
        self._cache = Cache(directory=os.path.join(user_cache_dir("giantpdf", "giantinc"), "PDFCache"))

        self._pdf_repository = PdfRepository(self._cache)

        self.single_page_display = SinglePage(message_signal, self._pdf_repository)
        self._display_service = DisplayService(display_strategy=self.single_page_display)

    def fetch_page_handler(self, file_path):
        Logger.info(f"Fetching text from page, {file_path}")
        cpu = cpu_count()
        doc = PdfRepository.open_pdf(file_path)
        PdfService.state['page_count'] = doc.page_count
        doc.close()

        PdfRenderWorker.run(
            cpu=cpu,
            filename=file_path,
            pdf_repository=self._pdf_repository,
            target=PdfRenderService.open_doc_in_pool
        )
        self._display_service.show_pdf_view(self._pdf_repository)

    def on_display_scroll_view(self):
        self._display_service.display_strategy = ScrollPage(self._signal)
        self._display_service.show_pdf_view(self._pdf_repository)

    def on_display_single_page_view(self):
        self._display_service.display_strategy = SinglePage(self._signal, self._pdf_repository)
        self._display_service.show_pdf_view(self._pdf_repository)

    def on_display_double_page_view(self):
        self._display_service.display_strategy = DoublePage(self._signal, self._pdf_repository)
        self._display_service.show_pdf_view(self._pdf_repository)

    def fetch_next_page_handler(self):
        Logger.debug(f"Fetching next page is the page count {json.dumps(PdfService.state)}")
        self._display_service.next_page()

    def fetch_prev_page_handler(self):
        self._display_service.prev_page()
