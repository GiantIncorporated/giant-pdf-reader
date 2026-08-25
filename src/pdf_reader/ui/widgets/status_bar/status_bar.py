from PySide6.QtWidgets import QStatusBar

from core.signals.bridge import Bridge
from ui.widgets.status_bar.tools.pdf_nav_buttons import PdfNavButtons
from ui.widgets.status_bar.tools.pdf_display_controls import PdfScaleSlider


class StatusBar(QStatusBar):
    def __init__(self, bridge:Bridge, parent=None):
        super().__init__(parent)
        self.setSizeGripEnabled(False)

        # Add PDF navigation buttons
        self._pdf_nav = PdfNavButtons(bridge)
        self.addWidget(self._pdf_nav, stretch=1)

        # Add pdf scale for zooming or scaling
        self._pdf_scale_slider = PdfScaleSlider(bridge)
        self.addWidget(self._pdf_scale_slider,)
