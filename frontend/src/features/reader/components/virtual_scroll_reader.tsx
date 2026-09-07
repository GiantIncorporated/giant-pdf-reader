// Virtual scrolling component for large PDFs
import PdfPage from "./pdf_page.tsx";
import type {PdfDoc} from "../../../types/reader.type.ts";
import {List} from 'react-window';
import {type RowComponentProps} from "react-window";
import {useMemo} from "react";

interface VirtualScrollReaderProps {
    pages: PdfDoc[]
    scale: number
}

function RowComponent({index, props, style}: RowComponentProps<{ props: VirtualScrollReaderProps }>) {
    const page = props.pages[index]
    return (
        <div style={style} className="flex justify-center py-2">
            <PdfPage scale={props.scale} payload={page}/>
        </div>
    )
}

export default function VirtualScrollReader({pages, scale}: VirtualScrollReaderProps) {
    // Calculate dynamic item height based on first page and scale
    const itemHeight = useMemo(() => {
        if (!pages.length) return 800
        const firstPage = pages[0]
        return Math.ceil((firstPage.canvas_height_px || 800) * (scale / 100)) + 16
    }, [pages, scale])


    return (
        <div className="w-full h-full overflow-hidden">
            <List
                rowHeight={itemHeight}
                rowCount={pages.length}
                rowComponent={RowComponent}
                rowProps={{
                    props: {
                        pages, scale
                    }
                }}/>
        </div>
    )
}