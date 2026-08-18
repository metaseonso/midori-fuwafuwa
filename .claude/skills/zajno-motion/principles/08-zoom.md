# Principle 8 — Zoom

> "Achieves smooth transitions between interface states while
> communicating depth and revealing hidden content."

## Why

Zoom is a transition that uses *scale + position* to traverse hierarchy.
Think Apple's app open animation, or scrolling Google Maps into a
neighborhood. Zoom answers "where am I in this content?" by physically
moving the camera, not by swapping pages.

## Three patterns

### a) **Card zoom-in to detail view** (the FLIP pattern)

The clicked element grows to fill the screen, becoming the next view.
Use GSAP Flip (covered in Principle 4) or shared-element transitions.

### b) **Scroll-driven hero zoom**

The hero image scales up as you scroll into it, revealing surrounding
content. ScrollTrigger handles this cleanly:

```js
gsap.to(".hero-img", {
  scale: 1.3,
  scrollTrigger: {
    trigger: ".hero",
    start: "top top",
    end: "bottom top",
    scrub: 1,                 // smoothed scrubbing (Zajno uses 1 or 3)
    pin: true,                // hold the hero in place while zoom plays
  },
});
```

### c) **Click-to-expand zoom** (lightbox / image zoom)

```js
function expand(img) {
  const state = Flip.getState(img);
  document.body.appendChild(img);                  // promote to top layer
  img.classList.add("is-expanded");                // CSS sets max width/height
  Flip.from(state, {
    duration: 0.6,
    ease: "power3.inOut",
    scale: true,                                   // animate scale, not width
  });
}
```

## Zoom-out reveal (the Zajno hero pattern)

This is one of motion.zajno.com's signature moves: start zoomed-in on a
detail, scroll causes camera to pull back revealing the bigger picture.
Same recipe as (b) but inverted:

```js
gsap.fromTo(".hero-img",
  { scale: 2.5 },                  // start zoomed IN
  {
    scale: 1,                      // pull back to normal
    scrollTrigger: {
      trigger: ".hero",
      start: "top top",
      end: () => "+=" + window.innerHeight,
      scrub: 1,
      pin: true,
      anticipatePin: 1,            // Zajno uses this — prevents pin flicker
    },
  }
);
```

Note `anticipatePin: 1` — extracted from Zajno's source, smooths the
moment the section pins.

## Rules

- Always pair zoom with `pin: true` if scroll-driven, otherwise the
  zoom finishes before the user can register it.
- `scrub: 1 – 3` (Zajno uses both). `scrub: true` (instant) feels too
  twitchy; `scrub: 3` is buttery but laggy on slow scrolls.
- Max scale jump: `0.5x → 2x` in one transition. Beyond that, the
  pixel quality breaks down on raster images.
- Use `transform-origin` to control *what* zooms toward you (default is
  center, but a hero photo often wants `center 30%`).

## Anti-patterns

- ❌ Zoom without pin → zoom finishes during scroll, user misses it
- ❌ `scrub: true` for slow content — feels jittery
- ❌ Zooming a `<video>` element above 1.5x — quality collapses
- ❌ Multiple competing zooms on the same scroll — pick one focal point
- ❌ Forgetting `transform: translateZ(0)` or `will-change: transform`
   on the zoomed element

See `examples/scroll-pinned-reveal.js`.
