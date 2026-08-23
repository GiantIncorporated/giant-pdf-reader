import platform

from PySide6.QtCore import QObject, Signal, Slot

from core.controllers.pdf_controller import PdfController
from core.utils.logging import Logger


class Bridge(QObject):
    messageReceived = Signal(str)
    scaleChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self._pdf_controller = PdfController(self.messageReceived)

    @Slot(str, result=str)
    def send_message(self, message: str) -> str:
        if not isinstance(message, str):
            raise TypeError("Message must be a string")
        response = f"Python received: {message!r}"
        self.messageReceived.emit(response)
        return response

    @Slot(int)
    def set_scale(self, scale: int) -> None:
        Logger.info(f"Setting scale to {scale}")
        self.scaleChanged.emit(scale)

    @Slot(str, result=str)
    def open_pdf_page(self, filepath) -> None:
        Logger.info(f"Fetching text from page, {filepath}")
        self._pdf_controller.fetch_page_handler(filepath)

    @Slot()
    def fetch_next_page(self) -> None:
        Logger.info(f"Fetching next page")
        self._pdf_controller.fetch_next_page_handler()

    @Slot()
    def fetch_prev_page(self) -> None:
        Logger.info(f"Fetching previous page")
        self._pdf_controller.fetch_prev_page_handler()


    @Slot(result=str)
    def get_system_info(self) -> str:
        return f"{platform.system()} {platform.release()} {platform.machine()}"
