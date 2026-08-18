# Timing System — durations, delays, stagger

Observed values from Zajno's source. Use these as defaults — adjust by feel.

## Duration scale

```js
const DURATION = {
  instant:  0.15,   // hover state changes, tooltips
  quick:    0.30,   // small UI (chips, badges, menu items)
  standard: 0.50,   // cards, modals, most reveals
  expressive: 0.70, // hero text, big reveals
  hero:     1.00,   // page-load hero, "wow moment" entries
  ambient:  2.00,   // smooth scroll (Lenis), looping background
};
```

Zajno's script contains these literal duration values: `0.2, 0.3, 0.4,
0.45, 0.5, 0.6, 0.7, 1` for tweens, and `2` for Lenis scroll. Outliers
(`4, 7, 8, 14, 18, 27`) are Lottie playback durations.

## Delay scale

```js
const DELAY = {
  none:     0,
  tight:    0.10,   // between two paired motions
  beat:     0.20,   // before a follow-up reveal
  pause:    0.40,   // dramatic pause (use sparingly)
};
```

## Stagger scale (Offset & Delay — Principle 2)

```js
const STAGGER = {
  tight: 0.04,   // 9–15 items, large grid
  base:  0.06,
  loose: 0.08,   // 4–8 items, deliberate reveal
  bold:  0.12,   // 2–4 items, each one demands attention
};
```

Rule of thumb: **total stagger duration ≤ 800ms**. If you have 20 items,
that means `0.04s` per item, not `0.12s`.

GSAP `stagger.amount` distributes a fixed total across all items —
useful for "spread this over 600ms regardless of count":

```js
gsap.from(".item", { y: 30, opacity: 0, stagger: { amount: 0.6 } });
```

## ScrollTrigger scrub values

Zajno uses two:

- `scrub: 1` — slight smoothing (cards, parallax)
- `scrub: 3` — buttery smoothing (long sections, big zooms)

`scrub: true` (no smoothing) is generally too twitchy.

## Mobile vs desktop

Zajno's breakpoint is `n > 991` (i.e., width > 991px = desktop).
On mobile they sometimes **halve durations** or skip the animation:

```js
const isDesktop = window.innerWidth > 991;
gsap.to(".el", {
  y: 0, opacity: 1,
  duration: isDesktop ? 0.7 : 0.4,
  delay:    isDesktop ? 0.2 : 0,
});
```

Also extracted from their source:
```js
duration: n > 991 ? 0.7 : 0
//                       ^ literally skip the animation on mobile
```

## The "responsiveness contract"

For interactive elements (hover, click, focus), aim for:
- Visual response within **100ms** of input
- Full transition complete within **300ms**

For reveals (scroll-triggered, page load), aim for:
- Each individual element: **300–700ms**
- Total choreography: under **2s** before content is fully visible

## Anti-patterns

- ❌ Hover transitions > 300ms — feels laggy
- ❌ Page-load reveals > 2s total — looks broken
- ❌ Same duration for every element — flatten hierarchy
- ❌ Sub-100ms transitions — user doesn't see the easing, just a jump
