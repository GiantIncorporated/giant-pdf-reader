# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-08-20
# Description: Provides methods for rendering PDF pages.
import base64
from dataclasses import asdict

from core.utils.logging import Logger
from features.pdf_display.repository.pdf_repository import PdfRepository
from features.pdf_display.services.render_service.pdf_service import PdfService


class PdfRenderService(PdfService):
    def __init__(self, pdf_repository):
        super().__init__(pdf_repository)


    @staticmethod
    def open_doc_in_pool(vector ):
        index = vector[0]
        cpu = vector[1]
        filename = vector[2]
        pdf_repository = vector[3]


        doc = PdfRepository.open_pdf(filename)
        page_count = doc.page_count

        seg_size = int(page_count / cpu + 1)
        seg_from = index * seg_size
        seg_to = min(seg_from + seg_size, page_count)

        for page_number in range(seg_from, seg_to):
            page = doc.load_page(page_number)
            spans = PdfRenderService.extract_text_spans(page)
            png_bytes, w, h = PdfRenderService.render_pixmap_without_text(page)
            is_saved = pdf_repository.save_pdf(
                page_number,
                page.rect.width,
                page.rect.height,
                w,
                h,
                base64.b64encode(png_bytes).decode('ascii'),
                [asdict(span) for span in spans],
                page_count,
            )
            if is_saved:
                Logger.debug(f"Page {page_number} saved")
        doc.close()

