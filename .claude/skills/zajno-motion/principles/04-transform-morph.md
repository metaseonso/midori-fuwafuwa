# Principle 4 — Transform & Morph

> "One object smoothly transforms into another shape, maintaining visual
> continuity and viewer focus."

## Why

When element A and element B are conceptually the same thing in different
states, *morphing* between them preserves the user's mental model. The eye
tracks one object instead of losing the connection between two.

Examples: hamburger ↔ close icon, play ↔ pause, plus ↔ minus,
search-icon ↔ search-input, card ↔ expanded-detail-view.

## Two flavors

### a) **CSS / transform morph** — same DOM node, animated properties

```js
// Hamburger to X
gsap.to(".bar-top", { y: 8, rotate: 45, duration: 0.3, ease: "power3.inOut" });
gsap.to(".bar-mid", { opacity: 0,        duration: 0.2 });
gsap.to(".bar-bot", { y: -8, rotate: -45, duration: 0.3, ease: "power3.inOut" });
```

### b) **SVG path morph** — true shape-to-shape interpolation

Requires GSAP's `MorphSVGPlugin` (Club GreenSock — paid) OR
[`flubber`](https://github.com/veltman/flubber) (free).

```js
import { MorphSVGPlugin } from "gsap/MorphSVGPlugin";
gsap.registerPlugin(MorphSVGPlugin);

gsap.to("#shape", {
  morphSVG: "#target-shape",
  duration: 0.6,
  ease: "power2.inOut",
});
```

Free alternative with `flubber`:

```js
import { interpolate } from "flubber";
const path = document.querySelector("#shape");
const tween = interpolate(currentD, targetD);
gsap.to({ t: 0 }, {
  t: 1, duration: 0.6, ease: "power2.inOut",
  onUpdate() { path.setAttribute("d", tween(this.targets()[0].t)); }
});
```

### c) **FLIP morph** — different DOM nodes, animate between layouts

This is what powers shared-element transitions (the "card grows into a
detail page" pattern). GSAP's Flip plugin is the cleanest:

```js
import { Flip } from "gsap/Flip";
gsap.registerPlugin(Flip);

const state = Flip.getState(".card");        // 1. snapshot
expandCard();                                  // 2. mutate the DOM
Flip.from(state, { duration: 0.6, ease: "power3.inOut" });  // 3. interpolate
```

## Rules

- The two states **must be conceptually the same thing**, not just visually similar
- Easing should be **in-out** (you're going from rest → rest, both endpoints matter)
- Duration: `0.3 – 0.6s` (longer feels like content, shorter like a glitch)
- Don't morph + fade simultaneously — pick one continuity strategy

## Anti-patterns

- ❌ Morphing between two unrelated icons (confuses, doesn't connect)
- ❌ Multi-step morphs without a hold beat at each state
- ❌ Using `power4.out` (ease-out) on a morph — it should be `inOut`
- ❌ Morphing on hover with > 200ms duration — feels laggy on a pointer

See `examples/morph-mask.js`.
