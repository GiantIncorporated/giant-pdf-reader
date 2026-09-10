from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QToolButton

from core.utils.helpers import load_stylesheet


class ToolButton(QToolButton):
    def __init__(self, text: str, icon_path: str, parent=None):
        super().__init__(parent)
        load_stylesheet(self,"tool_button.qss")
        self.setText(text)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(30,30))
        self.setFont(QFont("Roboto", 10))
        self.setAutoRaise(True)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

