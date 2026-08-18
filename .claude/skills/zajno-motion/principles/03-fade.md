# Principle 3 — Fade In / Fade Out

> "Objects appear or disappear through transparency-to-opacity transitions.
> Works best combined with position, scale, or form changes."

## Why

Fade alone is the weakest transition you can ship. The element doesn't go
anywhere — it just becomes visible. Pair it with motion (y/scale/blur) and
it becomes a *reveal*.

## The rule

**Never fade alone.** Always combine:

- `fade + y` (slide up + fade) → the safest, most common reveal
- `fade + scale` → for cards or hero images
- `fade + blur` → for premium hero content (expensive — use sparingly)
- `fade + x` → for sidebar / drawer entries

## How (GSAP)

```js
// Fade + slide up (the workhorse)
gsap.from(".reveal", {
  y: 30,
  opacity: 0,
  duration: 0.6,
  ease: "power2.out",
});

// Fade + scale (for cards)
gsap.from(".card", {
  scale: 0.92,
  opacity: 0,
  duration: 0.5,
  ease: "power3.out",
});

// Fade + blur (premium, GPU-heavy)
gsap.from(".hero-img", {
  opacity: 0,
  filter: "blur(20px)",
  duration: 0.8,
  ease: "power2.out",
});
```

## How (CSS)

```css
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 600ms ease-out, transform 600ms ease-out;
}
.reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
}
```

## How (Framer Motion)

```jsx
<motion.div
  initial={{ opacity: 0, y: 30 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-10%" }}
  transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
/>
```

## Timing reference (from Zajno's source)

- Hero reveals: `0.6 – 0.8s`
- Cards in a grid: `0.4 – 0.5s` (then staggered)
- Tooltips / micro-UI: `0.2 – 0.3s`
- Modal backdrop: `0.3s` fade-only is fine (it's a backdrop, not content)

## Anti-patterns

- ❌ `opacity 0 → 1` with no transform — invisible work, looks broken
- ❌ Fading text without `will-change: opacity` on long lists (jank)
- ❌ Fade duration > 1s for body content (feels slow)
- ❌ Fading something AND its parent — double fade reads as a bug
- ❌ Fading on every state change — only on *introductions*

See `examples/fade-with-transform.js`.
