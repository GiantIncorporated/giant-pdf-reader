# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-08-08
# Description: This class represents a PDF document and provides properties to access its various components such as page font,
#              page images, page text, and table of content.
from _pyrepl.utils import Span
from typing import List

class PdfDoc:
    def __init__(self,
                 page_number: int,
                 width_pt: float,
                 height_pt: float,
                 canvas_png_b64: str,
                 canvas_width_px: int,
                 canvas_height_px: int,
                 spans: List[Span],
                 page_count: int):
        self._page_number = page_number
        self._width_pt = width_pt
        self._height_pt = height_pt
        self._canvas_png_b64 = canvas_png_b64
        self._canvas_width_px = canvas_width_px
        self._canvas_height_px = canvas_height_px
        self._page_spans = spans
        self._page_count = page_count


    @property
    def width_pt(self):
        return self._width_pt

    @property
    def height_pt(self):
        return self._height_pt

    @property
    def canvas_png_b64(self):
        return self._canvas_png_b64

    @property
    def canvas_width_px(self):
        return self._canvas_width_px

    @property
    def canvas_height_px(self):
        return self._canvas_height_px

    @property
    def page_number(self):
        return self._page_number

    @property
    def page_spans(self):
        return self._page_spans

    @property
    def page_count(self):
        return self._page_count