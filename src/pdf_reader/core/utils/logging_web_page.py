from PySide6.QtWebEngineCore import QWebEnginePage
from pdf_reader.core.utils.logging import Logger
from typing import override


class LoggingWebPage(QWebEnginePage):

    @override
    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        Logger.info(f"[JS console] {source_id}:{line_number} — {message}")