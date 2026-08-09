// TextLayer.jsx

export default function TextLayer({spans, scale}: { spans: any[], scale: number }) {

    console.log('Spans of textLayer', spans)

    return (
        <div className="w-full h-full" style={{position: "absolute", top: 0, left: 0}}>
            {spans.map((span, i) => {
                const [x0, y0, x1, y1] = span.bounding_box;
                return (
                    <span
                        key={i}
                        data-span-index={i}
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
            {span.text}
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
