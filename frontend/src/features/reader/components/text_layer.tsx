// components/text_layer.tsx
interface TextLayerProps {
    spans: any[];
    scale: number;
}

export default function TextLayer({ spans, scale }: TextLayerProps) {

    return (
        <div className="text-layer" style={{ position: "absolute", top: 0, left: 0 }}>
            {spans.map((span, spanIndex) => {
                const [x0, y0, x1, y1] = span.bounding_box;
                return (
                    <span
                        key={spanIndex}
                        data-span-index={spanIndex}
                        className="pdf-text-span"
                        style={{
                            position: "absolute",
                            left: x0 * scale,
                            top: y0 * scale,
                            width: (x1 - x0) * scale,
                            height: (y1 - y0) * scale,
                            fontSize: span.font_size * scale,
                            fontFamily: span.font_name,
                            lineHeight: 1,
                            whiteSpace: "nowrap",
                            color: intToRgb(span.color),
                        }}
                    >
                        {Array.from(span.text).map((char:any, charIndex) => (
                            <span
                                key={charIndex}
                                className="pdf-text-char"
                                data-span-index={spanIndex}
                                data-char-index={charIndex}
                                style={{ display: "inline-block", opacity: 1 }}
                            >
                                {char === " " ? "\u00A0" : char}
                            </span>
                        ))}
                    </span>
                );
            })}
        </div>
    );
}

function intToRgb(colorInt: number) {
    const r = (colorInt >> 16) & 255;
    const g = (colorInt >> 8) & 255;
    const b = colorInt & 255;
    return `rgb(${r}, ${g}, ${b})`;
}