from typing import Optional, Callable

from PySide6 import QtCore
from PySide6.QtCore import QObject, Slot

from core.services.pdf_service import PdfService


class IpcTimers(QObject):
    def __init__(self):
        super().__init__()

        self._timer_send = QtCore.QTimer(self)
        self._timer_get = QtCore.QTimer(self)
        self._timer_waiting = QtCore.QTimer(self)

        self.timer_send.timeout.connect(self.on_timer_send)
        self.timer_get.timeout.connect(self.on_timer_get)
        self.timer_waiting.timeout.connect(self.on_timer_waiting)

        self._callback_send: Optional[Callable] = None
        self._callback_get: Optional[Callable] = None
        self._callback_waiting: Optional[Callable] = None

        self._start_time = 0

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def callback_send(self):
        return self._callback_send

    @callback_send.setter
    def callback_send(self,callback: Callable):
        self._callback_send = callback

    @property
    def callback_get(self):
        return self._callback_get

    @callback_get.setter
    def callback_get(self, callback: Callable):
        self._callback_get = callback

    @property
    def callback_waiting(self):
        return self._callback_waiting

    @callback_waiting.setter
    def callback_waiting(self, callback: Callable):
        self._callback_waiting = callback

    @property
    def timer_send(self):
        return self._timer_send

    @property
    def timer_get(self):
        return self._timer_get

    @property
    def timer_waiting(self):
        return self._timer_waiting

    @Slot()
    def on_timer_get(self):
        if self._callback_get:
            self._callback_get()

    @Slot()
    def on_timer_send(self):
        if self._callback_send:
            self._callback_send()

    @Slot()
    def on_timer_waiting(self):
        if self._callback_waiting:
            self._callback_waiting()
