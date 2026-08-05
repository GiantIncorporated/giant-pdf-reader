from PySide6 import QtCore
from PySide6.QtCore import QObject


class IpcTimers(QObject):
    def __init__(self):
        super().__init__()

        self._timer_send = QtCore.QTimer(self)
        self._timer_get = QtCore.QTimer(self)
        self._timer_waiting = QtCore.QTimer(self)

        self._start_time = 0

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def timer_send(self):
        return self._timer_send

    @property
    def timer_get(self):
        return self._timer_get

    @property
    def timer_waiting(self):
        return self._timer_waiting



