import json
import os
import queue
import time
from multiprocessing import Process, Queue
from typing import Any, Callable

from PySide6.QtCore import Signal

from core.services.pdf_render_service import PdfRenderService
from core.signals.ipc_timers import IpcTimers
from core.utils.logging import Logger


class PdfRenderWorker:
    """This class provides services for rendering PDF files."""

    def __init__(self,
                 signal: Signal,
                 render_service: PdfRenderService,
                 ) -> None:

        self._queue_number = Queue()
        self._queue_page_info = Queue()
        self._signal = signal

        self._process = None
        self._render_service = render_service

        self._ipc_timer = IpcTimers()
        self._ipc_timer.callback_get = lambda: self._render_service.fetch_rendered_page(
            self._queue_page_info,
            self._ipc_timer,
            self._signal
        )

        self._last_dir = ""
        self._file = None

    @property
    def queue_number(self):
        return self._queue_number

    @property
    def queue_page_info(self):
        return self._queue_page_info

    @property
    def ipc_timer(self):
        return self._ipc_timer

    def run(self, target: Callable[..., Any], args: tuple) -> None:
        """Render the PDF file."""
        (path, queue_number, queue_doc) = args
        if path:
            self._last_dir, self._file = os.path.split(path)
            if self._process:
                queue_number.put(-1)
            self._ipc_timer.timer_send.stop()
            self._render_service.current_page_number = 0
            self._render_service.page_count = 0
            self._process = Process(target=target,
                                    args=args)
            self._process.start()
            self._ipc_timer.timer_get.start(40)
            queue_number.put(0)
            self._ipc_timer.start_time = time.perf_counter()
            self._ipc_timer.timer_waiting.start(40)
