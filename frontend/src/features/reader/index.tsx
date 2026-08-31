import {useEffect, useRef} from "react";
import type {ReaderProps} from "../../types/reader.type.ts";
import TextLayer from "./components/text_layer.tsx";
import {useRevealAnimation} from "../../hooks/useRevealAnimation.ts";

const SCALAR = 100;

export default function Reader(props: { scale: number, payload: ReaderProps | null }) {

    const canvasRef = useRef<HTMLCanvasElement>(null);
    const pageContainerRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        if (!props.payload) return;
        console.log("This is the payload", props.payload)
        let isCurrent = true;
        const img = new Image();
        img.onload = () => {
            if (!isCurrent) return;
            const canvas = canvasRef.current;
            if (!canvas) return;
            canvas.width = props.payload?.canvas_width_px ?? 0;
            canvas.height = props.payload?.canvas_height_px ?? 0;
            const context = canvas.getContext('2d')
            if (!context) return;
            context.drawImage(img, 0, 0);
        };
        img.onerror = (e) => console.error("Image failed to load", e.toString(), props.payload?.canvas_png_b64?.slice(0, 50));
        if (!props.payload.canvas_png_b64) return;
        img.src = `data:image/png;base64,${props.payload.canvas_png_b64}`;
        return () => {
            isCurrent = false;
        };
    }, [props.payload]);

    useRevealAnimation(pageContainerRef, [props.payload?.page_number],{
        duration: 0.04,
        gapBetweenChars: 0.008
    });

    let scale = props.scale / SCALAR;

    return (
        <div className="flex justify-center items-center h-full">
            {
                props.payload ?
                    <div
                        className="mx-auto overflow-y-auto"
                        ref={pageContainerRef}
                        style={{
                            position: "relative",
                            width: props.payload?.width_pt ? props.payload.width_pt * scale : 1.2,
                            height: props.payload?.height_pt ? props.payload.height_pt * scale : 1.2,
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