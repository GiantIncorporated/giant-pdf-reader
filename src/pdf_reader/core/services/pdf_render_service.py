# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-07-31
# Description: Provides methods for rendering PDF pages.
import json
import queue

from core.repository.pdf_repository import PdfRepository
from core.services.pdf_service import PdfService
from core.utils.logging import Logger


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

    def fetch_rendered_page(self, queue_page_info, ipc_timer, signal):
        try:
            ret = queue_page_info.get(False)
            page_content = ""
            Logger.info(f"Using render service: {ret}")
            if isinstance(ret, int):
                ipc_timer.timer_waiting.stop()
                self.page_count = ret
                current_page_number = self.current_page_num + 1
                total_page_count = self.page_count
            else:
                (page_number, page_count, page_text) = ret
                current_page_number = page_number
                total_page_count = page_count
                page_content = page_text

            is_saved = self.save_pdf_in_repository(page_number=current_page_number,
                                                   page_text=page_content,
                                                   page_count=total_page_count
                                                   )
            if is_saved:
                pdf_doc = self.load_pdf_from_repository(current_page_number)
                payload = json.dumps({
                    "page_number": pdf_doc.page_number,
                    "page_count": pdf_doc.page_count,
                    "page_text": pdf_doc.page_text
                })
                signal.emit(payload)

        except queue.Empty as ex:
            pass
