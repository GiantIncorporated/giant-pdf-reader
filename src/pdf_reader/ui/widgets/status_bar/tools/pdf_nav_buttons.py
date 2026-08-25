from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QHBoxLayout, QWidget

from config import PACKAGE_ROOT
from features.pdf_display.signals.bridge import Bridge
from ui.widgets.buttons.button_with_icon import ButtonWithIcon

_ICON_DIR = PACKAGE_ROOT / "assets" / "icons"

class PdfNavButtons(QWidget):
    def __init__(self,bridge:Bridge):
        super().__init__()

        self._bridge = bridge

        self._h_layout = QHBoxLayout()
        self._h_layout.setContentsMargins(0, 0, 0, 0)
        self._h_layout.setSpacing(2)
        self._h_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        left_arrow_button = ButtonWithIcon("Left arrow", str(_ICON_DIR / "prev.png"))
        self._h_layout.addWidget(left_arrow_button)
        left_arrow_button.clicked.connect(self.on_prev_page_clicked)

        right_arrow_button = ButtonWithIcon("Right arrow", str(_ICON_DIR / "next.png"))
        right_arrow_button.clicked.connect(self.on_next_page_clicked)
        self._h_layout.addWidget(right_arrow_button)

        self.setLayout(self._h_layout)


    @Slot()
    def on_next_page_clicked(self):
        self._bridge.fetch_next_page()


    @Slot()
    def on_prev_page_clicked(self):
        self._bridge.fetch_prev_page()



