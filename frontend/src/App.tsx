import {useEffect, useState} from 'react'
import './App.css'
import {useWebChannel} from "./hooks/useWebChannel.ts";
import Reader from "./features/reader";
import type {ReaderProps} from "./types/reader.type.ts";

function App() {
    const {bridge, ready} = useWebChannel()
    const [filepath, setFilepath] = useState<string>('')
    const [pageNumber, setPageNumber] = useState<string>("0")
    const [sysInfo, setSysInfo] = useState<string>('')
    const [payload, setPayload] = useState<ReaderProps | null>(null)

    // Listen for Python-initiated pushes (Signal -> JS)
    useEffect(() => {
        if (!bridge) return

        const onMessage = (msg: string) => {
            let pageData = JSON.parse(msg)
            setPayload(pageData)
        }
        bridge.messageReceived.connect(onMessage)
        bridge.get_system_info((info) => setSysInfo(info))

        return () => {
            bridge.messageReceived.disconnect(onMessage)
        }
    }, [bridge])

    function handleSend() {
        if (!bridge || !filepath.trim()) return
        // Slot with result=str -> called with a JS callback for the return value
        bridge.open_pdf_page(filepath, () => {
            console.log(`You: ${filepath}`)
        })
    }

    function handleNextPage() {
        if (!bridge || !filepath.trim()) return
        // Slot with result=str -> called with a JS callback for the return value
        bridge.fetch_next_page(() => {
            console.log(`You: ${filepath}`, pageNumber)
        })
    }

    function hanglePrevPage() {
        if (!bridge || !filepath.trim()) return
        // Slot with result=str -> called with a JS callback for the return value
        bridge.fetch_prev_page(() => {
            console.log(`You: ${filepath}`, pageNumber)
        })
    }


    return (
        <div className="flex flex-col h-screen">
            <div className="relative h-32 flex-none">
                <div className="fixed shadow-md top-0 left-0 z-50 right-0 bg-white py-2">
                    <div className="flex flex-col gap-y-1">
                        <p className="text-lg">PySide6 + React + QWebChannel</p>
                        {sysInfo && <p className="text-sm text-gray-500">System: {sysInfo}</p>}
                    </div>

                    <div className="mb-2">
                        <input
                            className="border-2 rounded-sm px-2"
                            value={filepath}
                            onChange={(e) => setFilepath(e.target.value)}
                            placeholder="Type a message for Python..."
                        />
                    </div>
                    <div className="mb-2">
                        <input
                            className="border-2 rounded-sm px-2 hidden"
                            value={pageNumber}
                            onChange={(e) => setPageNumber(e.target.value)}
                            placeholder="Type a page number..."
                            type="number"
                        />
                    </div>
                    <div className="flex justify-center items-center px-2 gap-2">
                        <button type="button"
                                className="rounded-sm bg-indigo-600 px-2 py-1 text-xs font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:bg-indigo-500 dark:shadow-none dark:hover:bg-indigo-400 dark:focus-visible:outline-indigo-500"
                                onClick={hanglePrevPage} disabled={!ready}>
                            Prev
                        </button>
                        <button type="button"
                                className="rounded-sm bg-indigo-600 px-2 py-1 text-xs font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:bg-indigo-500 dark:shadow-none dark:hover:bg-indigo-400 dark:focus-visible:outline-indigo-500"
                                onClick={handleSend} disabled={!ready}>
                            Open
                        </button>
                        <button type="button"
                                className="rounded-sm bg-indigo-600 px-2 py-1 text-xs font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:bg-indigo-500 dark:shadow-none dark:hover:bg-indigo-400 dark:focus-visible:outline-indigo-500"
                                onClick={handleNextPage} disabled={!ready}>
                            Next
                        </button>
                    </div>

                </div>
            </div>
            <div className="bg-gray-200 py-2 grow">
                <Reader payload={payload}/>
            </div>

        </div>
    )
}

export default App
