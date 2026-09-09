export {}

declare global {
    interface QWebChannelTransport {
        send(message: string): void
        onmessage: ((message: MessageEvent) => void) | null
    }

    interface QWebChannelObjectSignal {
        connect(handler: (value: string) => void): void
        disconnect(handler: (value: string) => void): void
    }

    interface QWebChannelNumberSignal {
        connect(handler: (value: number) => void): void
        disconnect(handler: (value: number) => void): void
    }


    interface PdfReaderBridge {
        send_message(message: string, callback: (response: string) => void): void

        get_system_info(callback: (info: string) => void): void
        open_pdf_page(filepath: string, callback: (text: string) => void): void
        fetch_next_page(pageNumber:number): boolean
        fetch_prev_page(pageNumber: number): boolean

        messageReceived: QWebChannelObjectSignal
        scaleChanged: QWebChannelNumberSignal
        nextPage: QWebChannelObjectSignal
        prevPage: QWebChannelObjectSignal
    }

    interface QWebChannelInstance {
        objects: {
            bridge: PdfReaderBridge
        }
    }

    /**
     * QWebChannel constructor, injected at qrc:///qtwebchannel/qwebchannel.js.
     * Only available inside QWebEngineView — not in a plain browser.
     */
    const QWebChannel: {
        new(
            transport: QWebChannelTransport,
            callback: (channel: QWebChannelInstance) => void
        ): void
    }

    interface Window {
        qt?: {
            webChannelTransport: QWebChannelTransport
        }
    }
}