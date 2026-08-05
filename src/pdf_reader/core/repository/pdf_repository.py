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
    def __init__(self, cache:Cache):
        self._cache = cache

    @staticmethod
    def open_pdf(path):
        if not path:
            raise ValueError("Path cannot be empty")
        try:
            return pymupdf.open(path)
        except pymupdf.FileNotFoundError:
            return None


    def save_pdf(self,page_number:int, page_text:str, page_count:int):
        """Save rendered pdf file by worker in cache"""
        is_saved = self._cache.set(page_number, {
            "page_number": page_number,
            "page_text": page_text,
            "page_count":page_count,
        })
        if is_saved:
            return True
        return False

    def load_page(self, page_number) -> None | PdfDoc:
        """Load the rendered page data from the cache."""
        try:
            Logger.info("Loading page from pdf repository --start")
            response = self._cache.get(page_number)
            Logger.info(f"Loading page from pdf repository {response}")

            if not response:
                return None
            Logger.info(f"Loading page from pdf repository text {response['page_text']}")
            Logger.info(f"Loading page from pdf repository number {response['page_number']}")
            Logger.info(f"Loading page from pdf repository count {response['page_count']}")

            Logger.info("Loading page from pdf repository --end")
            pdf_doc = PdfDoc(page_text=response['page_text'],page_number=response['page_number'], page_count=response['page_count'])
            return pdf_doc
        except Exception as err:
            Logger.error(f"Error loading page from pdf repository: {err}")
            return None


    def clear_cache(self):
        """Clear the cache."""
        self._cache.clear()
