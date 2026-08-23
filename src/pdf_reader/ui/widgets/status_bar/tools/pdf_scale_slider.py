from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QSlider, QHBoxLayout

from core.signals.bridge import Bridge


class PdfScaleSlider(QWidget):
    def __init__(self, bridge:Bridge):
        super().__init__()
        self._bridge = bridge

        self._scale_slider = QSlider(Qt.Orientation.Horizontal)
        self._scale_slider.setMinimum(50)
        self._scale_slider.setMaximum(200)
        self._scale_slider.setValue(120)
        self._scale_slider.setTickInterval(20)
        self._scale_slider.setSingleStep(10)
        self._scale_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._scale_slider)
        self.setLayout(self._layout)


        self._scale_slider.valueChanged.connect(self._bridge.set_scale)
