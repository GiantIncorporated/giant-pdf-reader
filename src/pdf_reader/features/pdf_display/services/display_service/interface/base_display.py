from abc import ABC, abstractmethod

from features.pdf_display.repository.pdf_repository import PdfRepository


class BaseDisplay(ABC):
    @abstractmethod
    def display(self, pdf_repository: PdfRepository):
        pass

    @abstractmethod
    def prev_page(self):
        pass

    @abstractmethod
    def next_page(self):
        pass
