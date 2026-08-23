import {useEffect, useState} from 'react'
import './App.css'
import {useWebChannel} from "./hooks/useWebChannel.ts";
import Reader from "./features/reader";
import type {ReaderProps} from "./types/reader.type.ts";

function App() {
    const {bridge} = useWebChannel()
    const [, setSysInfo] = useState<string>('')
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


    return (
        <div className="flex flex-col h-screen">
            <div className="bg-gray-300 py-2 grow">
                <Reader payload={payload}/>
            </div>

        </div>
    )
}

export default App
