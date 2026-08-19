# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-07-27
# Description: This module provides services for reading and processing PDF files.
import json
from typing import override

from PySide6.QtCore import Signal

from core.models.pdf.pdf_doc import PdfDoc
from core.repository.pdf_repository import PdfRepository
from core.services.pdf_service import PdfService
from core.utils.logging import Logger


class PDFStorageService(PdfService):
    """This class provides services for reading and processing PDF files."""

    def __init__(self, pdf_repository: PdfRepository, signal: Signal):
        super().__init__(pdf_repository)
        self._pdf_repository = pdf_repository
        self._signal = signal


    @override
    def render_next_page(self, queue_page_num=None):
        Logger.debug(f"Rendering next page from storage {self.state["current_page_num"]} {self.state["page_count"]}")
        if self.state["current_page_num"] < self.state["page_count"]  - 1:
            Logger.info(f"Rendering next page from storage {self.state["current_page_num"]}")
            next_pdf_doc = self._pdf_repository.load_page(self.state["current_page_num"] + 1)
            if next_pdf_doc:
                self.state["current_page_num"] = self.state["current_page_num"] + 1
                self._emit_payload(payload=next_pdf_doc)
                return True
        return False

    @override
    def render_previous_page(self, queue_page_num=None):
        Logger.info("Rendering prev page from storage")
        if self.state["current_page_num"] > 0:
            prev_pdf_doc = self._pdf_repository.load_page(self.state["current_page_num"] - 1)
            if prev_pdf_doc:
                self.state["current_page_num"] = self.state["current_page_num"] - 1
                self._emit_payload(payload=prev_pdf_doc)
                return True
        return False

    def open_saved_doc(self, path, page_number):
        """Load the rendered page data from the cache."""
        Logger.info("fetching saved page")
        doc = PdfRepository.open_pdf(path)
        self.state["page_count"] = doc.page_count
        self.state["current_page_num"] = page_number
        pdf_doc = self._pdf_repository.load_page(page_number)
        if pdf_doc is None:
            return False
        self._emit_payload(payload=pdf_doc)
        return True

    def _emit_payload(self, payload:PdfDoc):
        file = json.dumps({
            "page_number": payload.page_number,
            "width_pt": payload.width_pt,
            "height_pt": payload.height_pt,
            "canvas_width_px": payload.canvas_width_px,
            "canvas_height_px": payload.canvas_height_px,
            "canvas_png_b64": payload.canvas_png_b64,
            "spans": payload.page_spans,
        })
        Logger.debug(f"sending page from storage text {file}")
        self._signal.emit(file)
