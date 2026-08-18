# Easing Curves — Zajno's actual palette

Extracted **verbatim** from `cdn.zajno.com/dev/motion/script.v33.min.js`
on 2026-05-23.

## Zajno's custom curves (verified)

```js
import { gsap } from "gsap";
import { CustomEase } from "gsap/CustomEase";
gsap.registerPlugin(CustomEase);

// Two-bump bounce — overshoots, recovers, settles
CustomEase.create(
  "bounce",
  "M0,0 C0.05222,-0.59802 0.31828,-1.38625 0.55039,0 0.65208,-0.78892 0.94566,-0.58262 1,1"
);

// Single-bump bounce — subtler, used for UI accents
CustomEase.create(
  "bounceSmall",
  "M0,0,C0.052,-0.598,0.246,-0.72,0.336,0,0.498,-0.502,0.792,-0.482,1,1"
);
```

Use them with `ease: "bounce"` or `ease: "bounceSmall"`.

## When to use which curve

| Curve in script             | When to use                                       |
|-----------------------------|---------------------------------------------------|
| `"none"`                    | Scrub-driven (`ScrollTrigger scrub`) only         |
| `"sine.out"`                | Subtle decel — secondary motion                   |
| `"bounce"`                  | Logo accents, CTA pulse — never on body content   |
| `"bounceSmall"`             | Hover-state confirmations                         |
| `"power2.out"`              | Default for entering elements (workhorse)         |
| `"power3.out"`              | Snappier entrance for snappy content              |
| `"power3.inOut"`            | Morphs (Principle 4), zooms (Principle 8)         |
| `"expo.out"`                | Long-distance hero moves (with `duration > 1s`)   |

## Lenis smooth-scroll easing (also Zajno-extracted)

```js
new Lenis({
  duration: 2,
  easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  // ^ This is the standard ease-out exponential. The 1.001 prevents the
  //   asymptote from making the scroll feel like it never quite arrives.
});
```

## CSS bezier equivalents

If you're not using GSAP, these `cubic-bezier()` values approximate
GSAP's popular eases:

| GSAP ease         | CSS `cubic-bezier(...)`                | What it feels like      |
|-------------------|----------------------------------------|-------------------------|
| `power2.out`      | `cubic-bezier(0.25, 1, 0.5, 1)`        | Soft arrival            |
| `power3.out`      | `cubic-bezier(0.33, 1, 0.68, 1)`       | Punchy arrival          |
| `power4.out`      | `cubic-bezier(0.16, 1, 0.3, 1)`        | "Premium" arrival       |
| `power2.inOut`    | `cubic-bezier(0.45, 0, 0.55, 1)`       | Symmetric ease          |
| `power3.inOut`    | `cubic-bezier(0.65, 0, 0.35, 1)`       | Strong symmetric ease   |
| `expo.out`        | `cubic-bezier(0.16, 1, 0.3, 1)`        | Long, smooth deceleration |
| `expo.inOut`      | `cubic-bezier(0.87, 0, 0.13, 1)`       | Dramatic in-out         |

## Easing decision tree

```
What kind of motion is this?

├── Entering view (reveal, mount)
│   └── ease-out family
│       ├── Quick UI?   → power2.out  (0.3 – 0.5s)
│       ├── Hero?       → power4.out / expo.out  (0.6 – 1.0s)
│       └── Playful?    → bounceSmall  (0.5 – 0.7s)
│
├── Leaving view (unmount, exit)
│   └── ease-in family
│       └── power2.in   (0.2 – 0.4s)
│
├── Both endpoints matter (morph, zoom, modal)
│   └── ease-in-out family
│       └── power3.inOut  (0.4 – 0.7s)
│
└── Bound to user scroll
    └── "none"  (linear — the user's scroll IS the easing)
```

## The "feel" rule

A page should have **at most 3 different eases** across all animations.
Pick one for entries, one for exits, one for hover/UI accents.
More than that and the motion language becomes incoherent.

Zajno's three:
1. `power2.out` / `power3.out` — entries
2. `power3.inOut` — morphs/zooms
3. `bounce` / `bounceSmall` — accents only
