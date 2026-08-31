import json
from typing import override

from PySide6.QtCore import Signal

from core.utils.logging import Logger
from features.pdf_display.models.pdf.pdf_doc import PdfDoc
from features.pdf_display.repository.pdf_repository import PdfRepository
from features.pdf_display.services.display_service.interface.base_display import BaseDisplay
from features.pdf_display.services.render_service.pdf_service import PdfService

class SinglePage(BaseDisplay):

    def __init__(self, signal: Signal, pdf_repository: PdfRepository):
        self._signal = signal
        self._pdf_repository = pdf_repository

    @override
    def display(self, pdf_repository: PdfRepository):
        pdf_doc = pdf_repository.load_single_page(0)
        PdfService.state['current_page_num'] = 0

        if pdf_doc is None:
            return

        self._emit_payload(payload=pdf_doc)

    @override
    def prev_page(self):
        state = PdfService.state
        if state["current_page_num"] > 0:
            prev_pdf_doc = self._pdf_repository.load_single_page(state["current_page_num"] - 1)
            if prev_pdf_doc:
                state["current_page_num"] = state["current_page_num"] - 1
                self._emit_payload(payload=prev_pdf_doc)
                return True
        return False

    @override
    def next_page(self):
        state =  PdfService.state
        Logger.debug(f"current page num {json.dumps(state)}")
        if state["current_page_num"] < state["page_count"] - 1:
            Logger.info(f"Rendering next page from storage {state["current_page_num"]}")
            next_pdf_doc = self._pdf_repository.load_single_page(state["current_page_num"] + 1)
            if next_pdf_doc:
                state["current_page_num"] = state["current_page_num"] + 1
                self._emit_payload(payload=next_pdf_doc)

    def _emit_payload(self, payload: PdfDoc):
        Logger.debug(f"sending page from storage text")
        self._signal.emit(json.dumps({
            "page_number": payload.page_number,
            "width_pt": payload.width_pt,
            "height_pt": payload.height_pt,
            "canvas_width_px": payload.canvas_width_px,
            "canvas_height_px": payload.canvas_height_px,
            "canvas_png_b64": payload.canvas_png_b64,
            "spans": payload.page_spans,
        }))




