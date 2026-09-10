from features.pdf_display.repository.pdf_repository import PdfRepository
from features.pdf_display.services.display_service.interface.base_display import BaseDisplay


class DisplayService:
    def __init__(self, display_strategy: BaseDisplay):
        self._display_strategy = display_strategy

    @property
    def display_strategy(self):
        return self._display_strategy

    @display_strategy.setter
    def display_strategy(self, display_strategy: BaseDisplay):
        self._display_strategy = display_strategy

    def show_pdf_view(self, pdf_repository: PdfRepository):
        self._display_strategy.display(pdf_repository)

    def prev_page(self, page_number)->bool:
        return self._display_strategy.prev_page(page_number)

    def next_page(self,page_number)->bool:
        return self._display_strategy.next_page(page_number)
