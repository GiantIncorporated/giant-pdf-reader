import os
import pdf_reader.config as config

from PySide6.QtCore import QUrl
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMainWindow

from core.signals.bridge import Bridge
from pdf_reader.core.utils.logging import Logger
from pdf_reader.core.utils.logging_web_page import LoggingWebPage
from ui.widgets.toolbar import  Toolbar


class MainWindow(QMainWindow):
    def __init__(self):
        Logger.info("Starting main window")
        super().__init__()
        self.setWindowTitle("Pdf Reader")
        self.resize(1200, 800)

        self.addToolBar(Toolbar())

        self._view = QWebEngineView()
        self._view.setPage(LoggingWebPage(self._view))
        self.setCentralWidget(self._view)

        self._channel = QWebChannel()
        self._bridge = Bridge()
        self._channel.registerObject('bridge', self._bridge)
        self._view.page().setWebChannel(self._channel)


        self._load_frontend()

    @property
    def view(self):
        return self._view

    @property
    def channel(self):
        return self._channel

    @property
    def bridge(self):
        return self._bridge

    def _load_frontend(self):
        Logger.info("Loading frontend")
        if config.DEV_MODE ==  config.DEVELOPMENT:
            self._view.load(QUrl( config.DEV_SERVER_URL))
            return
        Logger.info("Loading frontend from file")
        dist_index = os.path.abspath( config.PRODUCTION_PATH)
        if not os.path.exists(dist_index):
            Logger.error("No frontend found")
            raise FileNotFoundError(
                f"Could not find built frontend at {dist_index}.\n"
                "Run `npm install && npm run build` inside frontend/ first, "
                "or set DEV_MODE=1 and run `npm run dev` for local development."
            )
        Logger.info("Local file found")
        self._view.load(QUrl.fromLocalFile(dist_index))
