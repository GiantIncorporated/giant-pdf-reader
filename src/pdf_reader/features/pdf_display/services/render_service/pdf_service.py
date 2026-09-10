from typing import Any

from pymupdf import Page
from pymupdf import pymupdf, Rect, Matrix
from pymupdf._mupdf import PDF_REDACT_IMAGE_NONE

from features.pdf_display.models.pdf.text_span import TextSpan

TEXT_BLOCK = 0


class PdfService:

    state = {"page_count": 0, "current_page_num": 0, 'double_page_count': 0}
    double_pages = []

    def __init__(self, pdf_repository):
        self._pdf_repository = pdf_repository

    @staticmethod
    def render_pixmap_without_text(page: Page, zoom: float = 2.0) -> tuple[bytes, Any, Any]:
        doc = page.parent
        temp_doc = pymupdf.open()
        temp_doc.insert_pdf(doc, from_page=page.number, to_page=page.number)
        temp_page = temp_doc[0]

        text_dict = temp_page.get_text("dict")
        for block in text_dict["blocks"]:
            if block["type"] == TEXT_BLOCK:
                for line in block["lines"]:
                    for span in line["spans"]:
                        temp_page.add_redact_annot(Rect(span["bbox"]))
        temp_page.apply_redactions(images=PDF_REDACT_IMAGE_NONE)

        mat = Matrix(zoom, zoom)
        pix = temp_page.get_pixmap(matrix=mat, alpha=False)
        png_bytes = pix.tobytes("png")
        temp_doc.close()
        return png_bytes, pix.width, pix.height

    @staticmethod
    def extract_text_spans(page: Page) -> list[TextSpan]:
        spans = []
        text_dict = page.get_text("dict")
        for block in text_dict["blocks"]:
            if block["type"] != TEXT_BLOCK:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    spans.append(TextSpan(
                        text=span["text"],
                        bounding_box=span["bbox"],
                        font_size=span["size"],
                        font_name=span["font"],
                        color=span["color"],
                        flags=span["flags"]
                    ))

        return spans

    def save_pdf_in_repository(self, page_number, width_pt,
                               height_pt,
                               canvas_width_px,
                               canvas_height_px,
                               canvas_png_b64,
                               spans, page_count):
        return self._pdf_repository.save_pdf(page_number=page_number,
                                             width_pt=width_pt,
                                             height_pt=height_pt,
                                             canvas_width_px=canvas_width_px,
                                             canvas_height_px=canvas_height_px,
                                             canvas_png_b64=canvas_png_b64,
                                             spans=spans,
                                             page_count=page_count
                                             )

    def load_pdf_from_repository(self, page_number):
        return self._pdf_repository.load_page(page_number=page_number)
