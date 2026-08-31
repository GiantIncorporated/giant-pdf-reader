import os
import time
from multiprocessing import Process, Queue
from multiprocessing.pool import Pool
from typing import Any, Callable

from PySide6.QtCore import Signal

from features.pdf_display.services.render_service.pdf_render_service_old import PdfRenderService
from features.pdf_display.signals.ipc_timers import IpcTimers


class PdfRenderWorker:
    """This class provides services for rendering PDF files."""

    @staticmethod
    def run(cpu, filename, pdf_repository, target: Callable[..., Any]):
        vectors = [(i, cpu, filename, pdf_repository) for i in range(cpu)]
        pool = Pool()
        pool.map(target, vectors, 1)

