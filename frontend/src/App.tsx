import {useEffect, useState} from 'react'
import './App.css'
import {useWebChannel} from "./hooks/useWebChannel.ts";
import Reader from "./features/reader";

function App() {
    const {bridge, ready} = useWebChannel()
    const [filepath, setFilepath] = useState<string>('')
    const [pageNumber, setPageNumber] = useState<string>("0")
    const [log, setLog] = useState<string[]>([])
    const [sysInfo, setSysInfo] = useState<string>('')

    // Listen for Python-initiated pushes (Signal -> JS)
    useEffect(() => {
        if (!bridge) return

        const onMessage = (msg: string) =>{
            console.log(`This is the response data ${msg}`)
            let pageData = JSON.parse(msg)
            console.log(`This is the parsed response data ${msg}`)
            setLog((prev) => [...prev, pageData.page_text])
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
        bridge.fetch_text_from_page(filepath, pageNumber, () => {
            console.log(`You: ${filepath}`, pageNumber)
        })
    }


    return (
        <div className="bg-gray-200 h-screen overflow-y-auto py-2">
            <Reader />
        </div>
    )
}

export default App
