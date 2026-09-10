import json

from PySide6.QtCore import Signal
from typing_extensions import override

from core.utils.logging import Logger
from features.pdf_display.models.pdf.pdf_doc import PdfDoc
from features.pdf_display.repository.pdf_repository import PdfRepository
from features.pdf_display.services.display_service.interface.base_display import BaseDisplay
from features.pdf_display.services.render_service.pdf_service import PdfService


class DoublePage(BaseDisplay):

    def __init__(self, signal: Signal, pdf_repository: PdfRepository):
        self._signal = signal
        self._pdf_repository = pdf_repository

    @override
    def display(self, pdf_repository: PdfRepository, current_page: int = 0):
        pages = PdfService.double_pages[current_page]
        pdf_doc = pdf_repository.load_double_page(pages)
        PdfService.state['current_page_num'] = current_page + 1
        if pdf_doc is None or len(pdf_doc) == 0:
            return
        self._emit_payload(payload=pdf_doc)

    @override
    def next_page(self, page_number: int) -> bool:
        state = PdfService.state
        next_page = page_number + 1
        if next_page < PdfService.state['double_page_count']:
            pages = PdfService.double_pages[next_page]
            next_pdf_doc = self._pdf_repository.load_double_page(pages)
            if next_pdf_doc:
                state['current_page_num'] = next_page
                self._emit_payload(payload=next_pdf_doc)
                return True
        state['current_page_num'] = PdfService.state['double_page_count'] - 1
        return False

    @override
    def prev_page(self, page_number: int) -> bool:
        state = PdfService.state
        prev_page = page_number - 1
        if prev_page >= 0:
            pages = PdfService.double_pages[prev_page]
            prev_pdf_doc = self._pdf_repository.load_double_page(pages)
            if prev_pdf_doc:
                state["current_page_num"] = prev_page
                self._emit_payload(payload=prev_pdf_doc)
                return True
        state["current_page_num"] = 0
        return False

    def _emit_payload(self, payload: list[PdfDoc]):
        Logger.debug(f"sending page from storage text")
        pages = []
        for page in payload:
            parsed_page = DoublePage._parse_pdf_payload(page)
            pages.append(parsed_page)
        self._signal.emit(json.dumps({
            "type": "double_page",
            "currentPage": PdfService.state['current_page_num'],
            "fileName": PdfRepository.file_name,
            "fileDirectory": PdfRepository.file_path,
            "page_count": PdfService.state["page_count"],
            "pages": pages
        }))

    @staticmethod
    def _parse_pdf_payload(payload):
        return {
            "page_number": payload.page_number,
            "width_pt": payload.width_pt,
            "height_pt": payload.height_pt,
            "canvas_width_px": payload.canvas_width_px,
            "canvas_height_px": payload.canvas_height_px,
            "canvas_png_b64": payload.canvas_png_b64,
            "spans": payload.page_spans,
        }
