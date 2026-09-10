// Virtual scrolling component for large PDFs
import PdfPage from "./pdf_page.tsx";
import type {PdfDoc, ReaderProps} from "../../../types/reader.type.ts";
import {List} from 'react-window';
import {type RowComponentProps} from "react-window";
import {useMemo} from "react";

interface VirtualScrollReaderProps {
    pages: PdfDoc[],
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

export default function VirtualScrollReader({payload, scale}: { payload: ReaderProps, scale: number }) {
    // Calculate dynamic item height based on first page and scale
    const itemHeight = useMemo(() => {
        if (!payload.pages.length) return 800
        const firstPage = payload.pages[0]
        console.log('List payload count', payload?.page_count)
        console.log('List payload page count', payload.chunk)
        console.log(`virtual scrolling height, ${firstPage.canvas_height_px} `)
        return Math.ceil((firstPage.canvas_height_px || 800) * (scale / 100)) + 16
    }, [payload.pages, scale])


    return (
        <div className="w-full h-full overflow-hidden">
            <List
                rowHeight={itemHeight}
                rowCount={payload.page_count!}
                rowComponent={RowComponent}
                rowProps={{
                    props: {
                        pages: payload.pages, scale
                    }
                }}/>
        </div>
    )
}