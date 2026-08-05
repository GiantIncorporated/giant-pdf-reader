# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-07-31
# Description: Provides methods for rendering PDF pages.
import json
import multiprocessing as mp
import queue

from PySide6.QtCore import Slot, Signal

from core.repository.pdf_repository import PdfRepository
from core.signals.ipc_timers import IpcTimers
from core.utils.logging import Logger


class PdfRenderService:
    def __init__(self, pdf_repository, signal: Signal):
        self._queue_number = mp.Queue()
        self._queue_page_info = mp.Queue()
        self._page_count = 0
        self._current_page_num = 0
        self._pdf_repository = pdf_repository
        self._signal = signal

        self._ipc_timer = IpcTimers()

        self._ipc_timer.timer_send.timeout.connect(self.on_timer_send)
        self._ipc_timer.timer_get.timeout.connect(self.on_timer_get)
        self._ipc_timer.timer_waiting.timeout.connect(self.on_timer_waiting)

    @property
    def queue_number(self):
        return self._queue_number

    @property
    def queue_page_info(self):
        return self._queue_page_info

    @property
    def ipc_timer(self):
        return self._ipc_timer

    @property
    def page_count(self):
        return self._page_count

    @page_count.setter
    def page_count(self, value):
        self._page_count = value

    @property
    def current_page_num(self):
        return self._current_page_num

    @current_page_num.setter
    def current_page_num(self, value):
        self._current_page_num = value

    @staticmethod
    def open_doc_in_process(path, queue_number, queue_page_info):
        """Open the PDF document in the process."""
        doc = PdfRepository.open_pdf(path)
        page_count = doc.page_count
        queue_page_info.put(page_count)
        while True:
            page_number = queue_number.get()
            if page_number < 0:
                break
            page = doc.load_page(page_number)
            page_text = page.get_text("html")
            queue_page_info.put((page_number, page_count, page_text))
        doc.close()

    @Slot()
    def on_timer_get(self):
        self._fetch_rendered_page()

    def _fetch_rendered_page(self):
        try:
            ret = self.queue_page_info.get(False)
            page_content = ""
            Logger.info(f"Using render service: {ret}")
            if isinstance(ret, int):
                self._ipc_timer.timer_waiting.stop()
                self._page_count = ret
                current_page_number = self._current_page_num + 1
                total_page_count = self._page_count
            else:
                (page_number, page_count, page_text) = ret
                current_page_number = page_number
                total_page_count = page_count
                page_content = page_text

            is_saved = self._pdf_repository.save_pdf(page_number=current_page_number,
                                                     page_text=page_content,
                                                     page_count=total_page_count
                                                     )
            if is_saved:
                pdf_doc = self._pdf_repository.load_page(current_page_number)
                payload = json.dumps({
                    "page_number": pdf_doc.page_number,
                    "page_count": pdf_doc.page_count,
                    "page_text": pdf_doc.page_text
                })
                self._signal.emit(payload)

        except queue.Empty as ex:
            pass

    @Slot()
    def on_timer_waiting(self):
        self._showing_loading_progress()

    def _showing_loading_progress(self):
        pass

    @Slot()
    def on_timer_send(self):
        self._render_next_page()

    def _render_next_page(self):
        pass

    def render_entire(self):
        pass

    def render_previous_page(self):
        pass
