# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-07-27
# Description: This module provides a repository for PDF files.

import os

from diskcache import Cache
from pymupdf import pymupdf

from core.models.pdf.pdf_doc import PdfDoc
from core.utils.logging import Logger


class PdfRepository:
    def __init__(self, cache: Cache):
        self._cache = cache

    @staticmethod
    def open_pdf(path):
        if not path:
            raise ValueError("Path cannot be empty")
        try:
            return pymupdf.open(path)
        except pymupdf.FileNotFoundError:
            return None

    def save_pdf(self, page_number, width_pt,
                 height_pt,
                 canvas_width_px,
                 canvas_height_px,
                 canvas_png_b64,
                 spans, page_count):
        """Save rendered pdf file by worker in cache"""
        is_saved = self._cache.set(page_number, {
            "page_number": page_number,
            "width_pt": width_pt,
            "height_pt": height_pt,
            "canvas_width_px": canvas_width_px,
            "canvas_height_px": canvas_height_px,
            "canvas_png_b64": canvas_png_b64,
            "spans": spans,
            "page_count": page_count
        })
        if is_saved:
            return True
        return False

    def load_page(self, page_number) -> None | PdfDoc:
        """Load the rendered page data from the cache."""
        try:
            Logger.info("Loading page from pdf repository --start")
            response = self._cache.get(page_number)

            if not response:
                return None

            Logger.info("Loading page from pdf repository --end")
            pdf_doc = PdfDoc(
                page_number=response['page_number'],
                width_pt=response['width_pt'],
                height_pt=response['height_pt'],
                canvas_png_b64=response['canvas_png_b64'],
                canvas_width_px=response['canvas_width_px'],
                canvas_height_px=response['canvas_height_px'],
                spans=response['spans'],
                page_count=response['page_count']
            )
            return pdf_doc
        except Exception as err:
            Logger.error(f"Error loading page from pdf repository: {err}")
            return None

    def clear_cache(self):
        """Clear the cache."""
        self._cache.clear()
