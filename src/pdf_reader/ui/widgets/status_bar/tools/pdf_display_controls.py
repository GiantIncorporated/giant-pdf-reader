from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QSlider, QHBoxLayout, QButtonGroup, QToolButton

from config import PACKAGE_ROOT
from features.pdf_display.signals.bridge import Bridge
from ui.widgets.buttons.button_with_icon import ButtonWithIcon

_ICON_DIR = PACKAGE_ROOT / "assets" / "icons"


class PdfScaleSlider(QWidget):
    def __init__(self, bridge: Bridge):
        super().__init__()
        self._bridge = bridge

        self._scale_slider = QSlider(Qt.Orientation.Horizontal)
        self._scale_slider.setMinimum(50)
        self._scale_slider.setMaximum(200)
        self._scale_slider.setValue(120)
        self._scale_slider.setTickInterval(20)
        self._scale_slider.setSingleStep(10)
        self._scale_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self._button_group = QButtonGroup(self)

        single_page_button = ButtonWithIcon("Single page", str(_ICON_DIR / "single_page.png"))
        single_scrolling_button = ButtonWithIcon("Single scrolling", str(_ICON_DIR / "scroll_page.png"))
        double_page_button = ButtonWithIcon("Double page", str(_ICON_DIR / "double_page.png"))

        single_page_button.setCheckable(True)
        single_scrolling_button.setCheckable(True)
        double_page_button.setCheckable(True)

        self._button_group.addButton(single_page_button, id=0)
        self._button_group.addButton(double_page_button, id=1)
        self._button_group.addButton(single_scrolling_button, id=2)

        single_page_button.setChecked(True)

        self._layout = QHBoxLayout()
        self._layout.addWidget(single_page_button)
        self._layout.addWidget(double_page_button)
        self._layout.addWidget(single_scrolling_button)
        self._layout.addWidget(self._scale_slider)

        self.setLayout(self._layout)

        self._scale_slider.valueChanged.connect(self._bridge.set_scale)
        self._button_group.buttonClicked.connect(self._on_button_clicked)

    @Slot(int)
    def _on_button_clicked(self, button: QToolButton):
        pass
