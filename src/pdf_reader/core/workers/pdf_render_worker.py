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

        self._ipc_timer = IpcTimers()
        self._ipc_timer.callback_get = self._fetch_rendered_page


        self._process = None
        self._render_service = render_service
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

    def _fetch_rendered_page(self):
        try:
            ret = self.queue_page_info.get(False)
            page_content = ""
            Logger.info(f"Using render service: {ret}")
            if isinstance(ret, int):
                self._ipc_timer.timer_waiting.stop()
                self._page_count = ret
                current_page_number = self._render_service.current_page_num + 1
                total_page_count = self._page_count
            else:
                (page_number, page_count, page_text) = ret
                current_page_number = page_number
                total_page_count = page_count
                page_content = page_text

            is_saved = self._render_service.save_pdf_in_repository(page_number=current_page_number,
                                                     page_text=page_content,
                                                     page_count=total_page_count
                                                     )
            if is_saved:
                pdf_doc = self._render_service.load_pdf_from_repository(current_page_number)
                payload = json.dumps({
                    "page_number": pdf_doc.page_number,
                    "page_count": pdf_doc.page_count,
                    "page_text": pdf_doc.page_text
                })
                self._signal.emit(payload)

        except queue.Empty as ex:
            pass
