# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-07-31
# Description: Provides methods for rendering PDF pages.

from core.repository.pdf_repository import PdfRepository
from core.services.pdf_service import PdfService


class PdfRenderService(PdfService):
    def __init__(self, pdf_repository):
        super().__init__(pdf_repository)

    @staticmethod
    def open_doc_in_process(path, queue_number, queue_page_info):
        """Open the PDF document in the process."""
        doc = PdfRepository.open_pdf(path)
        page_count = doc.page_count
        queue_page_info.put(page_count)
        while True:
            page_number = queue_number.get()
            if page_number < 0:
                break
            page = doc.load_page(page_number)
            page_text = page.get_text("html")
            queue_page_info.put((page_number, page_count, page_text))
        doc.close()





