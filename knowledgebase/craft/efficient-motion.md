---
title: Efficient motion
tags: [craft, performance, motion, web]
status: settled
updated: 2026-08-19
source: research/case-study-01-immersive-efficiency.md
---

# Efficient motion

One idea, applied at every layer: **push work onto the browser's compositor, and off the main
thread.**

## Three rules, no exceptions

1. **Animate `transform` and `opacity` only.** Nothing else. Anything touching layout — width,
   height, top, margin — forces reflow on the main thread and causes jank.
2. **Native CSS scroll-driven animation is primary.** `animation-timeline: scroll()` / `view()` with
   `animation-range`. Compositor-only, no scroll listener, no `requestAnimationFrame` loop, no
   `getBoundingClientRect()` polling.
3. **GSAP + Lenis is the secondary layer only** — for choreography CSS timelines cannot express:
   pinned sections, scrubbed sequences, staggered batches.

## Why native CSS wins

Chrome's own case study showed the JS-listener equivalent going janky under main-thread load while
the CSS version stayed smooth. Because scroll timelines only ever touch `transform` and `opacity`,
they run on the compositor, fully decoupled from whatever JavaScript is doing.

**Browser support:** solid in Chrome/Edge and Safari 26. Firefox lags.

**The honest fallback:** `@supports (animation-timeline: scroll())` with a **static state**
underneath. **Not a JS polyfill** — a polyfill would put the work back on the main thread and cancel
out the entire performance win.

## GSAP discipline, when it is used

- `transform` / `opacity` only, same as everything else.
- `will-change` only on elements *actively* animating — leaving it on permanently wastes memory.
- `ScrollTrigger.batch()` instead of per-element triggers.
- Tune `scrub` with a numeric lag rather than binding 1:1 to raw scroll.
- **Read DOM values, then write them. Never interleave.** Interleaving is what causes layout
  thrashing.
- Lenis (~4KB) smooths native scroll input **without hijacking the scrollbar** — which is why it was
  chosen over Locomotive Scroll.

## WebGL is seasoning, not the meal

Reserve it for a single deliberate accent per [[field-and-forest|Field]].

- Mount the canvas only on scroll-into-view (`IntersectionObserver`).
- `frameloop="demand"` — render on change, not a continuous 60fps loop.
- Drop pixel ratio during interaction, restore at idle.
- Compress geometry and textures: Draco/meshopt cut mesh size 90%+; KTX2/Basis keep textures
  GPU-compressed instead of ballooning in VRAM.
- **Skip it entirely under reduced motion** — see [[reduced-motion-first]].

## The bigger point for this studio

**The art style is already the efficient choice.** Flat, chibi, hand-illustrated work is one of the
cheapest things to render beautifully. Layered PNG/SVG art parallaxing at different scroll speeds
reads as rich and dreamlike while staying compositor-cheap.

Efficiency is not a constraint fighting the immersive goal here. They are the same choice.

## Related

- [[reduced-motion-first]] — the baseline state
- [[asset-export-rules]] — the layer before any animation code runs
- [[field-and-forest]] — what this motion is for
- [[../../brand/DESIGN_SYSTEM|DESIGN_SYSTEM.md §4]] — the actual duration and easing tokens
