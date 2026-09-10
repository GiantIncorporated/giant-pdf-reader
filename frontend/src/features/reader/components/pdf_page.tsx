import {useEffect, useRef} from "react";
import TextLayer from "./text_layer.tsx";
import type {PdfDoc} from "../../../types/reader.type.ts";

const SCALAR = 100;
const imageCache = new Map<string, ImageData>();

// Create worker once at module level
let decodeWorker: Worker | null = null;

function getDecodeWorker() {
    if (!decodeWorker) {
        decodeWorker = new Worker('/pdf-decode-worker.js');
    }
    return decodeWorker;
}

export default function PdfPage(props: { scale: number, payload: PdfDoc | null }) {

    const canvasRef = useRef<HTMLCanvasElement>(null);
    const pageContainerRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        if (!props.payload?.canvas_png_b64) return;
        let isCurrent = true;

        const cacheKey = `page_${props.payload.page_number}`;
        if (imageCache.has(cacheKey)) {
            drawToCanvas(canvasRef.current, imageCache.get(cacheKey)!);
            return;
        }

        // Decode base64 on MAIN thread, send bitmap to worker
        const binaryString = atob(props.payload.canvas_png_b64);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }

        const blob = new Blob([bytes], {type: 'image/png'});

        // createImageBitmap works in both main thread and workers
        createImageBitmap(blob).then((imageBitmap) => {
            if (!isCurrent) return;
            const worker = getDecodeWorker();
            worker.postMessage(
                {
                    imageBitmap,
                    width: props.payload!.canvas_width_px,
                    height: props.payload!.canvas_height_px,
                },
                [imageBitmap] // Transfer ownership
            );
        });

        const handleMessage = (e: MessageEvent) => {
            if (!isCurrent) return;
            if (e.data.success) {
                const imageData = e.data.imageData;
                imageCache.set(cacheKey, imageData);
                drawToCanvas(canvasRef.current, imageData);
            }
        };

        const worker = getDecodeWorker();
        worker.addEventListener('message', handleMessage);

        return () => {
            isCurrent = false;
            worker.removeEventListener('message', handleMessage);
        };
    }, [props.payload]);
    const scale = props.scale / SCALAR;

    return (
        <div className="flex justify-center items-center h-full">
            {
                props.payload ?
                    <div
                        className="mx-auto overflow-y-auto"
                        ref={pageContainerRef}
                        style={{
                            position: "relative",
                            width: (props.payload?.width_pt ?? 0) * scale,
                            height: (props.payload?.height_pt ?? 0) * scale,
                        }}
                    >
                        <canvas
                            ref={canvasRef}
                            style={{
                                position: "absolute",
                                top: 0,
                                left: 0,
                                width: "100%",
                                height: "100%",
                                imageRendering: "crisp-edges",
                            }}
                        />
                        <TextLayer spans={props.payload.spans} scale={scale}/>
                    </div>
                    :
                    <div className="mx-auto flex justify-center items-center h-full">
                        Please insert a valid PDF file.
                    </div>
            }
        </div>
    );
}

function drawToCanvas(canvas: HTMLCanvasElement | null, imageData: ImageData) {
    if (!canvas) return;
    canvas.width = imageData.width;
    canvas.height = imageData.height;
    const ctx = canvas.getContext('2d');
    if (ctx) {
        ctx.putImageData(imageData, 0, 0);
    }
}