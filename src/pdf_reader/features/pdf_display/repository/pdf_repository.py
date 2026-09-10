# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-08-20
# Description: This module provides a repository for PDF files.

from diskcache import Cache
from pymupdf import pymupdf

from features.pdf_display.models.pdf.pdf_doc import PdfDoc
from core.utils.logging import Logger


class PdfRepository:

    file_path: str
    file_name: str

    def __init__(self, cache: Cache):
        self._cache = cache

    @staticmethod
    def open_pdf(path):
        if not path:
            raise ValueError("Path cannot be empty")
        try:
            PdfRepository.file_path = path
            PdfRepository.file_name = path.split("/")[-1]
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

    def load_single_page(self, page_number) -> None | PdfDoc:
        """Load the single page data from the cache."""
        try:
            Logger.info("Loading page from pdf repository --start")
            response = self._cache.get(page_number)

            if not response:
                return None

            pdf_doc = PdfRepository._get_pdf_doc(response)
            Logger.debug(f"Loaded pdf page from repository {page_number}")
            return pdf_doc
        except Exception as err:
            Logger.error(f"Error loading page from pdf repository: {err}")
            return None

    @staticmethod
    def paginate_double(items, items_per_page=2):
        pages = []
        for i in range(0, len(items), items_per_page):
            pages.append(items[i:i + items_per_page])
        return pages

    def load_double_page(self, page_number: tuple[int, int]) -> None | list[PdfDoc]:
        try:
            Logger.info("Loading page from pdf repository --start")
            pages = []
            first_page = self._cache.get(page_number[0])
            if first_page is None:
                return None

            first_pdf_doc = PdfRepository._get_pdf_doc(first_page)
            pages.append(first_pdf_doc)

            second_page = self._cache.get(page_number[1])

            if second_page is None:
                return pages

            second_pdf_doc = PdfRepository._get_pdf_doc(second_page)
            pages.append(second_pdf_doc)

            return pages
        except Exception as err:
            Logger.error(f"Error loading page from pdf repository: {err}")
            return None

    def load_scroll_page(self, page_count ):
        try:
            Logger.info("Loading page from pdf repository --start")
            pages = []
            for page_number in range(page_count):
                response = self._cache.get(page_number)
                if not response:
                    break
                pdf_doc = PdfRepository._get_pdf_doc(response)
                pages.append(pdf_doc)
                Logger.debug(f"Loaded pdf page from repository {page_number}")
            return pages
        except Exception as err:
            Logger.error(f"Error loading page from pdf repository: {err}")
            return None

    @staticmethod
    def _get_pdf_doc(pdf_page) -> PdfDoc:
        return PdfDoc(
            page_number=pdf_page['page_number'],
            width_pt=pdf_page['width_pt'],
            height_pt=pdf_page['height_pt'],
            canvas_png_b64=pdf_page['canvas_png_b64'],
            canvas_width_px=pdf_page['canvas_width_px'],
            canvas_height_px=pdf_page['canvas_height_px'],
            spans=pdf_page['spans'],
            page_count=pdf_page['page_count']
        )

    def clear_cache(self):
        """Clear the cache."""
        self._cache.clear()
