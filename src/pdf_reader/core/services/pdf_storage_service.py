# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-07-27
# Description: This module provides services for reading and processing PDF files.
import json

from PySide6.QtCore import Signal

from core.models.pdf.pdf_doc import PdfDoc
from core.repository.pdf_repository import PdfRepository 
from core.utils.logging import Logger


class PDFStorageService:
    """This class provides services for reading and processing PDF files."""

    def __init__(self, pdf_repository: PdfRepository, signal:Signal):
        self._pdf_repository = pdf_repository
        self._signal = signal

    def render_next_page(self):
        pass

    def render_prev_page(self):
        pass

    def store_rendered_page(self, page: PdfDoc):
        """Save the rendered page data to the cache."""
        self._pdf_repository.save_pdf(page_number=page.page_number, page_text=page.page_text,
                                      page_count=page.page_count)

    def fetch_saved_page(self, page_number):
        """Load the rendered page data from the cache."""
        Logger.info("fetching saved page")
        page = self._pdf_repository.load_page(page_number)
        if page is None:
            return False
        payload = json.dumps({
            "page_number": page.page_number,
            "page_count": page.page_count,
            "page_text": page.page_text
        })
        Logger.info(f"sending page from storage text {page.page_text}")
        self._signal.emit(payload)
        return True
