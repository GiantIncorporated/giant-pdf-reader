import {useEffect, useRef} from "react";

export default function Reader() {

    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        if (!ctx) return;
        ctx.fillStyle = 'red';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }, []);

    return (
        <div className="w-1/2 min-w-0 mx-auto bg-white h-full">
            <canvas ref={canvasRef}/>
        </div>
    );
}