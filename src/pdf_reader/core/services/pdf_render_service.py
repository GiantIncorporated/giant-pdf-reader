# Author: Enoch Viewu
# Date Created: 2026-07-26
# Last Modified: 2026-08-08
# Description: Provides methods for rendering PDF pages.
import base64
import json
import queue
from dataclasses import asdict

from typing_extensions import override

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
            spans = PdfRenderService.extract_text_spans(page)
            png_bytes, w, h = PdfRenderService.render_pixmap_without_text(page)
            queue_page_info.put((
                page_number,
                page.rect.width,
                page.rect.height,
                w,
                h,
                base64.b64encode(png_bytes).decode('ascii'),
                [asdict(span) for span in spans],
                page_count,
            ))
        doc.close()

    def fetch_rendered_page(self, queue_page_info, ipc_timer, signal):
        try:
            ret = queue_page_info.get(False)
            page_content = []
            width_point = None
            height_point = None
            canvas_width_pix = None
            canvas_height_pix = None
            canvas_png_img_b64 = None

            Logger.info(f"Using render service")
            if isinstance(ret, int):
                ipc_timer.timer_waiting.stop()
                self.page_count = ret
                self.current_page_num = self.current_page_num + 1
                total_page_count = self.page_count
            else:
                (page_number, width_pt, height_pt,
                 canvas_width_px, canvas_height_px,
                 canvas_png_b64, spans, page_count) = ret

                width_point = width_pt
                height_point = height_pt
                canvas_width_pix = canvas_width_px
                canvas_height_pix = canvas_height_px
                canvas_png_img_b64 = canvas_png_b64
                self.current_page_num = page_number
                total_page_count = page_count
                page_content = spans

            is_saved = self.save_pdf_in_repository(
                page_number=self.current_page_num,
                width_pt=width_point,
                height_pt=height_point,
                canvas_width_px=canvas_width_pix,
                canvas_height_px=canvas_height_pix,
                canvas_png_b64=canvas_png_img_b64,
                spans=page_content,
                page_count=total_page_count
            )
            if is_saved:
                pdf_doc = self.load_pdf_from_repository(self.current_page_num)
                Logger.debug(f"PDF document saved")
                payload = json.dumps({
                    "page_number": pdf_doc.page_number,
                    "width_pt": pdf_doc.width_pt,
                    "height_pt": pdf_doc.height_pt,
                    "canvas_width_px": pdf_doc.canvas_width_px,
                    "canvas_height_px": pdf_doc.canvas_height_px,
                    "canvas_png_b64": pdf_doc.canvas_png_b64,
                    "spans": pdf_doc.page_spans,
                })
                signal.emit(payload)

        except queue.Empty as ex:
            pass

    @override
    def render_next_page(self, queue_page_num=None):
        if self.current_page_num < self.page_count - 1:
            queue_page_num.put(self.current_page_num + 1)

    @override
    def render_previous_page(self, queue_page_num=None):
        if self.current_page_num > 0:
            queue_page_num.put(self.current_page_num - 1)
