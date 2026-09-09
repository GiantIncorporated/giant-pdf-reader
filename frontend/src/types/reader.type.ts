export interface ReaderProps {
    type: string;
    currentPage: number;
    fileName: string;
    fileDirectory: string;
    page_count: number;
    chunk?: number;
    total_chunks?: number;
    start_page?: number;
    end_page?: number;
    parse_duration_ms?:number;
    pages: PdfDoc[];
}

export interface PdfDoc {
    page_number: number,
    width_pt: number,
    height_pt: number,
    canvas_width_px: number,
    canvas_height_px: number,
    canvas_png_b64: string,
    spans: any,
    payload: any
}