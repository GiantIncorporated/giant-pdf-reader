import {useEffect, useState} from 'react'
import './App.css'
import {useWebChannel} from "./hooks/useWebChannel.ts";
import Reader from "./features/reader";
import type {ReaderProps} from "./types/reader.type.ts";

function App() {
    const {bridge} = useWebChannel()
    const [payload, setPayload] = useState<ReaderProps | null>(null)
    const [scale, setScale] = useState<number>(100)

    // Listen for Python-initiated pushes (Signal -> JS)
    useEffect(() => {
        if (!bridge) return

        const onMessage = (msg: string) => {
            let pageData = JSON.parse(msg)
            setPayload(pageData)
        }
        bridge.messageReceived.connect(onMessage)

        const onScaleChanged = (scale: number) => setScale(scale)
        bridge.scaleChanged.connect(onScaleChanged)

        return () => {
            bridge.messageReceived.disconnect(onMessage)
            bridge.scaleChanged.disconnect(onScaleChanged)
        }
    }, [bridge])


    return (
        <div className="flex flex-col h-screen">
            <div className="bg-gray-300 py-2 grow">
                <Reader scale={scale} payload={payload}/>
            </div>

        </div>
    )
}

export default App
