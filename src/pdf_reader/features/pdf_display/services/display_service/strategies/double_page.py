from PySide6.QtCore import Signal
from typing_extensions import override

from features.pdf_display.repository.pdf_repository import PdfRepository
from features.pdf_display.services.display_service.interface.base_display import BaseDisplay
from features.pdf_display.services.render_service.pdf_service import PdfService
from features.pdf_display.services.render_service.pdf_storage_service import PDFStorageService


class DoublePage(BaseDisplay):

    def __init__(self, signal: Signal, pdf_repository: PdfRepository):
        self._signal = signal
        self._pdf_repository = pdf_repository

    @override
    def display(self, pdf_repository: PdfRepository):
        pdf_doc = pdf_repository.load_double_page(0)

    @override
    def next_page(self):
        pass

    @override
    def prev_page(self):
        pass

