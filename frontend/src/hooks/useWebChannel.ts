import {useEffect, useState} from "react";

let channelPromise: Promise<QWebChannelInstance> | null = null

function getWebChannel(): Promise<QWebChannelInstance> {
    if (channelPromise) return channelPromise

    channelPromise = new Promise((resolve, reject) => {
        if (typeof window.qt === 'undefined' || !window.qt.webChannelTransport) {
            reject(new Error('qt.webChannelTransport not found — not running inside QWebEngineView?'))
            return
        }
        new QWebChannel(window.qt.webChannelTransport, (channel) => {
            resolve(channel)
        })
    })

    return channelPromise
}

export function useWebChannel() {
    const [bridge, setBridge] = useState<PdfReaderBridge | null>(null)
    const [ready, setReady] = useState(false)

    useEffect(() => {
        let cancelled = false

        getWebChannel()
            .then((channel) => {
                if (cancelled) return
                setBridge(channel.objects.bridge)
                setReady(true)
            })
            .catch((err: Error) => {
                console.warn('[useWebChannel]', err.message)
            })

        return () => {
            cancelled = true
        }
    }, [])

    return {bridge, ready}
}