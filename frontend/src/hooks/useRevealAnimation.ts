// hooks/useRevealAnimation.ts
import {useEffect, useRef, type RefObject} from "react";
import {gsap} from "gsap";

interface RevealAnimationOptions {
    /** Selector for the smallest animatable unit — now individual characters */
    selector?: string;
    /** How long each character takes to fade from 0 -> 1 opacity */
    duration?: number;
    /** Gap between one character finishing and the next starting */
    gapBetweenChars?: number;
    ease?: string;
    delay?: number;
    disabled?: boolean;
    onCharComplete?: (index: number, el: HTMLElement) => void;
    onComplete?: () => void;
}

export function useRevealAnimation<T extends HTMLElement>(
    containerRef: RefObject<T | null>,
    deps: unknown[] = [],
    options: RevealAnimationOptions = {}
) {
    const {
        selector = ".pdf-text-char",
        duration = 0.01,
        gapBetweenChars = 0.01,
        ease = "sine.inOut",
        delay = 0,
        disabled = false,
        onCharComplete,
        onComplete,
    } = options;

    const timelineRef = useRef<gsap.core.Timeline | null>(null);

    useEffect(() => {
        if (disabled) return;
        const container = containerRef.current;
        if (!container) return;

        // Order matters: querySelectorAll returns nodes in DOM order, which —
        // because TextLayer renders spans/chars in the order PyMuPDF extracted them
        // (left-to-right, top-to-bottom per line) — already gives left-to-right reveal
        // across the page without any extra sorting.
        const chars = Array.from(
            container.querySelectorAll<HTMLElement>(selector)
        );
        if (chars.length === 0) return;

        timelineRef.current?.kill();

        const prefersReducedMotion = window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

        gsap.set(chars, {opacity: 0});

        if (prefersReducedMotion) {
            gsap.set(chars, {opacity: 1});
            onComplete?.();
            return;
        }

        const tl = gsap.timeline({delay, onComplete});
        timelineRef.current = tl;

        chars.forEach((char, index) => {
            tl.to(char, {
                opacity: 1,
                duration,
                ease,
                onComplete: () => onCharComplete?.(index, char),
            }, index === 0 ? undefined : `+=${gapBetweenChars}`);
        });

        return () => {
            tl.kill();
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [
        containerRef,
        selector,
        duration,
        gapBetweenChars,
        ease,
        delay,
        disabled,
        ...deps,
    ]);

    return timelineRef;
}