# Principle 6 — Dimension (Floating Dimensionality)

> "Conveys volume and depth through layered movement, creating intuitive,
> narrative-rich interactions."

## Why

The web is 2D, but the user's perception is 3D. "Dimension" is the
technique of *implying* depth through layered motion — without resorting
to drop shadows or skeuomorphism. Done well, it makes elements feel like
objects floating in space.

## Building blocks

1. **Layer separation** — divide content into z-depth layers (background,
   mid, foreground). Each layer moves at a different rate.
2. **Differential motion** — when the user scrolls, hovers, or moves the
   pointer, layers respond proportionally to their implied depth.
3. **Subtle 3D rotation** — small `rotateX` / `rotateY` (max ±8°) on hover
   gives the "card lifts toward you" feel.

## How (pointer-driven dimension)

```js
const card = document.querySelector(".dim-card");
const layers = card.querySelectorAll("[data-depth]");

card.addEventListener("mousemove", (e) => {
  const rect = card.getBoundingClientRect();
  const x = (e.clientX - rect.left) / rect.width  - 0.5;  // -0.5 .. 0.5
  const y = (e.clientY - rect.top)  / rect.height - 0.5;

  // Tilt the whole card slightly
  gsap.to(card, {
    rotateY: x * 8,
    rotateX: -y * 8,
    duration: 0.4, ease: "power2.out",
    transformPerspective: 1000,
  });

  // Move each layer by its depth
  layers.forEach(layer => {
    const depth = parseFloat(layer.dataset.depth); // e.g. 0.2, 0.5, 1.0
    gsap.to(layer, {
      x: x * 40 * depth, y: y * 40 * depth,
      duration: 0.4, ease: "power2.out",
    });
  });
});

card.addEventListener("mouseleave", () => {
  gsap.to(card,   { rotateY: 0, rotateX: 0, duration: 0.6, ease: "power3.out" });
  gsap.to(layers, { x: 0, y: 0,              duration: 0.6, ease: "power3.out" });
});
```

```html
<div class="dim-card" style="transform-style: preserve-3d;">
  <div data-depth="0.2"><img src="bg.jpg"  alt="" /></div>
  <div data-depth="0.5"><img src="mid.png" alt="" /></div>
  <div data-depth="1.0"><h2>Foreground text</h2></div>
</div>
```

## How (scroll-driven dimension)

This is technically Parallax (Principle 7). See `examples/parallax-layers.js`.

## Rules

- Max tilt: **±8°**. More than that and it's no longer subtle — it's a
  toy effect.
- Always pair tilt with `transformPerspective` (1000–1500px works).
- Smooth the response with `duration: 0.3 – 0.5s, ease: power2.out` —
  not instant (jitter) and not slow (laggy).
- Reset on `mouseleave` with a longer, slower ease so the card
  "settles" back rather than snapping.
- Respect `prefers-reduced-motion` — disable tilt entirely for users
  who've set this preference.

## Anti-patterns

- ❌ Tilt > 15° — looks like a broken game
- ❌ No reset animation — card stays tilted after pointer leaves
- ❌ Animating without `will-change: transform` on the card (causes jank)
- ❌ Using `rotateZ` for "dimension" — that's not depth, that's spinning
- ❌ Forgetting `transform-style: preserve-3d` on the parent

See `examples/dimension-layers.js`.
