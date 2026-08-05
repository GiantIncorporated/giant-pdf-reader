# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-07-26
# Description: This class represents a PDF document and provides properties to access its various components such as page font,
#              page images, page text, and table of content.

class PdfDoc:
    def __init__(self,
                 page_text: str,
                 page_number: int,
                 page_count: int):
        self._page_number = page_number
        self._page_text = page_text
        self._page_count = page_count


    @property
    def page_number(self):
        return self._page_number

    @property
    def page_text(self):
        return self._page_text

    @property
    def page_count(self):
        return self._page_count