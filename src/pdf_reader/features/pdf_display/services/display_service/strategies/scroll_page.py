from typing import override

from PySide6.QtCore import Signal

from features.pdf_display.repository.pdf_repository import PdfRepository
from features.pdf_display.services.display_service.interface.base_display import BaseDisplay


class ScrollPage(BaseDisplay):

    def __init__(self, signal: Signal):
        self._signal = signal

    @override
    def display(self, pdf_repository: PdfRepository):
        pdf_pages = pdf_repository.get_pdf_pages()

        if len(pdf_pages) == 0:
            return

        for page in pdf_pages:
            self._signal.emit(page)

    @override
    def prev_page(self):
        pass

    @override
    def next_page(self):
        pass