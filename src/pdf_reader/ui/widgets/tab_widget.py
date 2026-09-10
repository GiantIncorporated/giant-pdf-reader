from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout

from core.utils.helpers import load_stylesheet


class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        load_stylesheet(self, "tab_widget.qss")

    def add_tab(self, widget, title):
        """Adds a new tab to the tab widget."""
        self.addTab(widget, title)

    def remove_tab(self, index):
        """Removes a tab from the tab widget."""
        self.removeTab(index)


