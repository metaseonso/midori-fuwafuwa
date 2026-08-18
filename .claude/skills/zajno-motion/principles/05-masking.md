# Principle 5 — Masking

> "Uses morphing objects as masks for photographs or content; masked
> elements can scale, move, or spin."

## Why

A mask reveals content *through a shape*. Instead of the boring
"fade-in-photo", you get a reveal with personality — the photo emerges
from inside a circle, a stripe, a custom blob, an SVG path. Masking
gives the studio-quality moment that distinguishes premium sites.

## Three techniques

### a) **CSS `clip-path`** — the modern web standard

```css
.reveal {
  clip-path: inset(0 100% 0 0);                    /* hidden, clipped from right */
  transition: clip-path 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.reveal.is-visible {
  clip-path: inset(0 0 0 0);                       /* fully revealed */
}

/* Circular reveal: */
.reveal { clip-path: circle(0% at 50% 50%); }
.reveal.is-visible { clip-path: circle(100% at 50% 50%); }
```

```js
// GSAP version
gsap.fromTo(".reveal",
  { clipPath: "inset(0 100% 0 0)" },
  { clipPath: "inset(0 0 0 0)", duration: 0.8, ease: "power3.out" }
);
```

### b) **SVG `<mask>` or `<clipPath>`** — for custom shapes

```html
<svg width="0" height="0">
  <defs>
    <clipPath id="blob" clipPathUnits="objectBoundingBox">
      <path d="M0.5,0 C0.78,0 1,0.22 1,0.5 C1,0.78 0.78,1 0.5,1 C0.22,1 0,0.78 0,0.5 C0,0.22 0.22,0 0.5,0 Z"/>
    </clipPath>
  </defs>
</svg>

<img src="hero.jpg" style="clip-path: url(#blob);" />
```

You can then morph the clip-path itself (combine with Principle 4).

### c) **Overlay slide** — fake mask via a sliding panel

When `clip-path` isn't an option (old browsers, complex content),
slide a solid panel over/off the content:

```js
gsap.from(".reveal-wrap > .overlay", {
  scaleX: 0,
  transformOrigin: "right center",
  duration: 0.7,
  ease: "power3.inOut",
});
```

This is the classic "wipe reveal" used on agency hero sections.

## Rules

- **Mask animates, content stays still** (usually). Or vice versa. Not both.
- The mask shape should *mean something* — a circle on a hero photo is a
  visual lens; a horizontal stripe is a curtain pull. Random shapes feel arbitrary.
- Duration: `0.6 – 0.9s` (masks are deliberate, not snappy).
- Easing: `power3.inOut` or `cubic-bezier(0.83, 0, 0.17, 1)`.

## Anti-patterns

- ❌ Masking with `overflow: hidden` + width animation on `<img>` — causes
   the image content to *scale*, not reveal. Use `clip-path` instead.
- ❌ Masking AND fading the same element (one continuity strategy at a time)
- ❌ `clip-path: polygon(…)` morphs without `will-change: clip-path` (jank)
- ❌ Animating SVG `<mask>` with `<animate>` tags — GSAP is more controllable

See `examples/morph-mask.js`.
