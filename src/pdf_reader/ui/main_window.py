# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-08-20
# Description: The main window of the application

import os

from PySide6.QtCore import QUrl
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QStatusBar

import pdf_reader.config as config
from core.signals.bridge import Bridge
from core.utils.helpers import load_stylesheet
from pdf_reader.core.utils.logging import Logger
from pdf_reader.core.utils.logging_web_page import LoggingWebPage
from ui.widgets.status_bar.status_bar import StatusBar
from ui.widgets.status_bar.tools.pdf_nav_buttons import PdfNavButtons
from ui.widgets.tab_widget import TabWidget
from ui.widgets.toolbars.home_toolbar import HomeToolbar



class MainWindow(QMainWindow):
    def __init__(self):
        Logger.info("Starting main window")
        super().__init__()
        load_stylesheet(self, "global.qss")

        self._channel = QWebChannel()
        self._bridge = Bridge()
        self._channel.registerObject('bridge', self._bridge)

        self.setWindowTitle("Pdf Reader")
        self.resize(1200, 800)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._widget = QWidget()

        self._setup_tab_toolbar()
        self._setup_status_bar()

        self._view = QWebEngineView()
        self._view.setPage(LoggingWebPage(self._view))
        self._view.page().setWebChannel(self._channel)
        self._layout.addWidget(self._view)

        self._widget.setLayout(self._layout)
        self.setCentralWidget(self._widget)

        self._load_frontend()


    def _setup_status_bar(self):
        self._statusbar = StatusBar(self._bridge)
        self.setStatusBar(self._statusbar)


    def _setup_tab_toolbar(self):
        tab_widget = TabWidget()
        home_toolbar = HomeToolbar(self._bridge)
        tab_widget.add_tab(home_toolbar, "Home")

        self._layout.addWidget(tab_widget)



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
        if config.DEV_MODE == config.DEVELOPMENT:
            self._view.load(QUrl(config.DEV_SERVER_URL))
            return
        Logger.info("Loading frontend from file")
        dist_index = os.path.abspath(config.PRODUCTION_PATH)
        if not os.path.exists(dist_index):
            Logger.error("No frontend found")
            raise FileNotFoundError(
                f"Could not find built frontend at {dist_index}.\n"
                "Run `npm install && npm run build` inside frontend/ first, "
                "or set DEV_MODE=1 and run `npm run dev` for local development."
            )
        Logger.info("Local file found")
        self._view.load(QUrl.fromLocalFile(dist_index))


    def closeEvent(self, event, /):
        event.accept()
        super().closeEvent(event)
