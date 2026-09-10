import {useEffect, useState} from 'react'
import './App.css'
import {useWebChannel} from "./hooks/useWebChannel.ts";
import Reader from "./features/reader";
import type {PdfDoc} from "./types/reader.type.ts";
import {useDispatch, useSelector} from "react-redux";
import {nextPage, prevPage, savePdf} from "./features/reader/pdfSlice.ts";

function App() {
    const {bridge} = useWebChannel()
    const [scale, setScale] = useState<number>(100)
    const payload = useSelector((state: any) => state.pdf.pdfFile)
    const dispatch = useDispatch()

    // Listen for Python-initiated pushes (Signal -> JS)
    useEffect(() => {
        if (!bridge) return

        const onMessage = (msg: string) => {
            let pageData = JSON.parse(msg)
            console.log("Received message:", pageData)
            if (pageData.type === 'scroll_page') {
                // setPayload((prev) => {
                //         if (!prev) {
                //             return {
                //                 ...pageData,
                //                 type: pageData.type,
                //                 pages: pageData.pages || [],
                //             }
                //         }
                //
                //         const newPages = [...(prev.pages || []), ...pageData.pages]
                //         const seen = new Set<number>()
                //         const deduped = newPages.filter((page: PdfDoc) => {
                //             if (seen.has(page.page_number)) return false
                //             seen.add(page.page_number)
                //             return true
                //         })
                //
                //         return {
                //             ...pageData,
                //             type: pageData.type,
                //             pages: deduped,
                //         }
                //
                //     }
                // )
                // return
            }
            console.log(`Received page data: ${pageData.pages}`)
            dispatch(savePdf(pageData))
        }
        bridge.messageReceived.connect(onMessage)

        const onScaleChanged = (scale: number) => setScale(scale)
        bridge.scaleChanged.connect(onScaleChanged)

        const onNextPage = () => {
            const currentPage = payload.currentPage
            console.log(`Current page in on next page: ${currentPage}`)
            const pdfPage = bridge.fetch_next_page(currentPage)
            if (pdfPage) {
                console.log("Received next page data:", pdfPage)
                dispatch(nextPage())
            }
        }
        bridge.nextPage.connect(onNextPage)

        const onPrevPage = () => {
            const currentPage = payload.currentPage
            console.log(`Current page in on prev page: ${currentPage}`)
            const pdfPage = bridge.fetch_prev_page(currentPage)
            if (pdfPage) {
                console.log("Received prev page data:", pdfPage)
                dispatch(prevPage())
            }
        }
        bridge.prevPage.connect(onPrevPage)


        return () => {
            bridge.messageReceived.disconnect(onMessage)
            bridge.scaleChanged.disconnect(onScaleChanged)
            bridge.nextPage.disconnect(onNextPage)
            bridge.prevPage.disconnect(onPrevPage)
        }
    }, [bridge,payload])


    return (
        <div className="flex flex-col h-screen">
            <div className="bg-gray-300 py-2 grow">
                <Reader scale={scale} payload={payload}/>
            </div>

        </div>
    )
}

export default App
