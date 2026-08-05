import platform

from PySide6.QtCore import QObject, Signal, Slot

from core.controllers.pdf_controller import PdfController
from core.utils.logging import Logger


class Bridge(QObject):
    messageReceived = Signal(str)

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

    @Slot(str, int, result=str)
    def fetch_text_from_page(self, filepath, page_number) -> None:
        Logger.info(f"Fetching text from page, {filepath} {page_number}")
        self._pdf_controller.fetch_page_handler(filepath, page_number)


    @Slot(result=str)
    def get_system_info(self) -> str:
        return f"{platform.system()} {platform.release()} {platform.machine()}"
