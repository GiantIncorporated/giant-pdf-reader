from abc import ABC, abstractmethod


class BaseDisplay(ABC):
    @abstractmethod
    def show(self, pdf_page):
        pass
