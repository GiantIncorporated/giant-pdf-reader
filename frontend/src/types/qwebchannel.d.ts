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

    interface PdfReaderBridge {
        send_message(message: string, callback: (response: string) => void): void
        get_system_info(callback: (info: string) => void): void
        open_pdf_page(filepath: string, page_number: string, callback: (text: string) => void): void
        fetch_next_page(callback: (text: string) => void): void
        fetch_prev_page(callback: (text: string) => void): void
        add(a: number, b: number, callback: (sum: number) => void): void
        messageReceived: QWebChannelObjectSignal
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