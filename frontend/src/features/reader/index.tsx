import type { PdfDoc, ReaderProps } from "../../types/reader.type.ts";
import PdfPage from "./components/pdf_page.tsx";
import classNames from "../../utils/class_names.ts";
import VirtualScrollReader from "./components/virtual_scroll_reader.tsx";


interface IReader {
    scale: number;
    payload: ReaderProps | null;
}

export default function Reader({ scale, payload }: IReader) {
    const currentPage = payload?.pages ?? []

    if (!payload || !currentPage.length) {
        return (
            <div className="flex justify-center items-center h-full">
                Please insert a valid PDF file.
            </div>
        )
    }

    // Use virtual scrolling for large PDFs (50+ pages)
    if (currentPage.length > 14) {
        console.log(`Using virtual scrolling, ${payload.pages.length} `)
        console.log('in reader payload page count', payload.chunk)
        return <VirtualScrollReader payload={payload} scale={scale} />
    }

    // Normal rendering for small PDFs
    return (
        <div className={classNames(
            payload.type === "double_page" ? "gap-x-4" : "flex-col gap-y-1",
            "flex justify-center items-center h-full"
        )}>
            {currentPage.map((page: PdfDoc) => (
                <div key={page.page_number}>
                    <PdfPage scale={scale} payload={page} />
                </div>
            ))}
        </div>
    )
}

