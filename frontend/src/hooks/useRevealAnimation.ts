// hooks/useRevealAnimation.ts
import { useEffect, useRef, type RefObject } from "react";
import { gsap } from "gsap";

interface RevealAnimationOptions {
    selector?: string;
    /** How long each individual span takes to fade from 0 -> 1 opacity */
    duration?: number;
    /** Gap between one span finishing its fade and the next starting */
    gapBetweenSpans?: number;
    ease?: string;
    delay?: number;
    disabled?: boolean;
    onSpanComplete?: (index: number, el: HTMLElement) => void;
    onComplete?: () => void;
}

export function useRevealAnimation<T extends HTMLElement>(
    containerRef: RefObject<T | null>,
    deps: unknown[] = [],
    options: RevealAnimationOptions = {}
) {
    const {
        selector = ".pdf-text-span",
        duration = 0.3,
        gapBetweenSpans = 0.05,
        ease = "sine.inOut",
        delay = 0,
        disabled = false,
        onSpanComplete,
        onComplete,
    } = options;

    const timelineRef = useRef<gsap.core.Timeline | null>(null);

    useEffect(() => {
        if (disabled) return;
        const container = containerRef.current;
        if (!container) return;

        const spans = Array.from(
            container.querySelectorAll<HTMLElement>(selector)
        );
        if (spans.length === 0) return;

        timelineRef.current?.kill();

        const prefersReducedMotion = window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

        // All text is present in the DOM immediately, just invisible —
        // this is what makes it "display at opacity 0" rather than not rendered at all
        gsap.set(spans, { opacity: 0.2 });

        if (prefersReducedMotion) {
            gsap.set(spans, { opacity: 1 });
            onComplete?.();
            return;
        }

        const tl = gsap.timeline({ delay, onComplete });
        timelineRef.current = tl;

        spans.forEach((span, index) => {
            tl.to(span, {
                opacity: 1,
                duration,       // the gradual increase happens here, over `duration` seconds
                ease,           // "sine.inOut" gives a smooth ramp rather than linear/instant
                onComplete: () => onSpanComplete?.(index, span),
            });
            if (index < spans.length - 1) {
                tl.to({}, { duration: gapBetweenSpans });
            }
        });

        return () => {
            tl.kill();
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [
        containerRef,
        selector,
        duration,
        gapBetweenSpans,
        ease,
        delay,
        disabled,
        ...deps,
    ]);

    return timelineRef;
}