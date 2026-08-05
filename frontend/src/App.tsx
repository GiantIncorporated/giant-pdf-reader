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

        //     <div className="bg-gray-200 h-screen overflow-y-auto py-2">
        //     <Reader />
        // </div>


    return (
        <div className="app">
            <h1>PySide6 + React + QWebChannel</h1>
            <p className="status">
                {ready ? '🟢 connected to Python' : '🟡 waiting for bridge...'}
            </p>
            {sysInfo && <p className="sysinfo">System: {sysInfo}</p>}

            <div>
                <input
                    value={filepath}
                    onChange={(e) => setFilepath(e.target.value)}
                    placeholder="Type a message for Python..."
                />
            </div>
            <div>
                <input
                    value={pageNumber}
                    onChange={(e) => setPageNumber(e.target.value)}
                    placeholder="Type a page number..."
                    type="number"
                />
            </div>
            <button onClick={handleSend} disabled={!ready}>
                Send
            </button>

            <div className="log">
                {log.map((line, i) => (
                    <div key={i} dangerouslySetInnerHTML={{__html: line}} ></div>
                ))}
            </div>
        </div>
    )
}

export default App
