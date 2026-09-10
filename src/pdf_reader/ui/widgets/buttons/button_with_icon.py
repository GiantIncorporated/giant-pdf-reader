from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QToolButton

from core.utils.helpers import load_stylesheet


class ButtonWithIcon(QToolButton):
    def __init__(self, text: str, icon_path: str, parent=None):
        super().__init__(parent)
        load_stylesheet(self, "icon_only_button.qss")
        self.setToolTip(f"{text} button")
        self.setIcon(QIcon(icon_path))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setAutoRaise(True)