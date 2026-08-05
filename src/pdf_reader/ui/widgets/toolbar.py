
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QToolBar, QFileDialog

from config import PACKAGE_ROOT

_ICON_DIR = PACKAGE_ROOT / "assets" / "icons"
_STYLES_dir = PACKAGE_ROOT / "assets" / "styles"


class Toolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._load_stylesheet()

        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setMovable(False)

        self._open_action = QAction(QIcon(str(_ICON_DIR / "open.png")), "Open", self)
        self._open_action.triggered.connect(self._open_file)
        self.addAction(self._open_action)

    def _load_stylesheet(self):
        qss_path = _STYLES_dir/"toolbar.qss"
        try:
            self.setStyleSheet(qss_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            pass

    def _open_file(self):
        path, _ = QFileDialog.getOpenFileName(self,
                                              "Open File", "",
                                              "PDF Files (*.pdf)")