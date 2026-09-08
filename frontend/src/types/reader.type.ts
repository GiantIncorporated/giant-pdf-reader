export interface ReaderProps {
    type: string;
    pages: PdfDoc[]
    chunk?: number
    total_chunks?: number
    start_page?: number
    end_page?: number
    page_count?: number
    parse_duration_ms?: number
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