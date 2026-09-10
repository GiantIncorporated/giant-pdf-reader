from abc import ABC, abstractmethod

from features.pdf_display.repository.pdf_repository import PdfRepository


class BaseDisplay(ABC):
    @abstractmethod
    def display(self, pdf_repository: PdfRepository, current_page: int = 0):
        pass

    @abstractmethod
    def prev_page(self, page_number:int)->bool:
        pass

    @abstractmethod
    def next_page(self, page_number:int)->bool:
        pass
