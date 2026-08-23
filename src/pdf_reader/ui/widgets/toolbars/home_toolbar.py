from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QHBoxLayout, QWidget, QFileDialog

from config import PACKAGE_ROOT
from core.signals.bridge import Bridge
from core.utils.logging import Logger
from ui.widgets.buttons.tool_button import ToolButton

_ICON_DIR = PACKAGE_ROOT / "assets" / "icons"

class HomeToolbar(QWidget):
    def __init__(self, bridge: Bridge):
        super().__init__()
        self._bridge = bridge

        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(2, 0, 2, 0)
        self._layout.setSpacing(0)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.open_button = ToolButton("Open",  str(_ICON_DIR / "open.png"))
        self.open_button.clicked.connect(self.on_open)

        self._layout.addWidget(self.open_button)

        self.setLayout(self._layout)


    @Slot()
    def on_open(self):
        Logger.info("Open button clicked")
        path, _ = QFileDialog.getOpenFileName(self,
                                              "Open File", "",
                                              "PDF Files (*.pdf)")
        self._bridge.open_pdf_page(path)