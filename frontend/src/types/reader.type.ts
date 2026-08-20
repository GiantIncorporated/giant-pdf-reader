export interface ReaderProps {
    page_number: number,
    width_pt: number,
    height_pt: number,
    canvas_width_px: number,
    canvas_height_px: number,
    canvas_png_b64: string,
    spans: any,
    payload: any
}