# Principle 1 — Easing

> "In nature, the speed of movement is never linear: objects gain speed as
> they begin to move, and slow as they come to a halt."
> — Zajno

## Why

Linear motion looks robotic. Eased motion looks alive. This is the single
highest-leverage change you can make to a UI — replace every `linear`
transition with an `ease` and the product instantly feels more premium.

## Easing types (Zajno's vocabulary)

| Type      | Curve description                          | Use for                                |
|-----------|--------------------------------------------|----------------------------------------|
| `linear`  | Constant speed                             | Almost never. Loading bars maybe.      |
| `ease`    | Slight accel start, decel end              | Generic transitions, safe default      |
| `ease-in` | Slow start, accelerates                    | Element exiting offscreen              |
| `ease-out`| Quick start, slows at end                  | Element entering — feels arrival       |
| `cubic`   | Extended accel + decel (very smooth)       | Long-distance hero moves               |

## How (GSAP)

```js
gsap.to(".card", { y: 0, opacity: 1, duration: 0.6, ease: "power2.out" });
//                                                  ^^^^^^^^^^^^^^^^^^
//                                                  this is the win
```

**Zajno's actual custom curves** (lifted verbatim from their site):

```js
import CustomEase from "gsap/CustomEase";
gsap.registerPlugin(CustomEase);

CustomEase.create("bounce",
  "M0,0 C0.05222,-0.59802 0.31828,-1.38625 0.55039,0 0.65208,-0.78892 0.94566,-0.58262 1,1");

CustomEase.create("bounceSmall",
  "M0,0,C0.052,-0.598,0.246,-0.72,0.336,0,0.498,-0.502,0.792,-0.482,1,1");

// Use:
gsap.to(".cta", { scale: 1, duration: 0.5, ease: "bounce" });
```

## How (CSS)

```css
.card {
  transition: transform 600ms cubic-bezier(0.16, 1, 0.3, 1); /* ease-out cubic */
}
```

## Anti-patterns

- ❌ `transition: all 0.3s linear`
- ❌ Same easing for arrival AND departure — arrival = `ease-out`, exit = `ease-in`
- ❌ Mixing 5 different eases on one page — pick 2–3 max
- ❌ Using `bounce`/`elastic` everywhere — they're seasoning, not the meal

## Decision tree

```
Element entering view? → ease-out (decelerating into place)
Element leaving view?  → ease-in  (accelerating away)
Element repositioning? → ease (in-out)
Want playful?          → bounce / bounceSmall (sparingly)
```

See `references/easing-curves.md` for the full palette and
`examples/custom-easing.js` for the registration snippet.
