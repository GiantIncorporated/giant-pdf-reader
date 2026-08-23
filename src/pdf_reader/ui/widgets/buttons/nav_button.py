from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QToolButton


class NavButton(QToolButton):
    def __init__(self, text: str, icon_path: str, parent=None):
        super().__init__(parent)
        self.setToolTip(f"{text} button")
        self.setIcon(QIcon(icon_path))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setAutoRaise(True)