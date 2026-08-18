# Principle 2 — Offset & Delay (Stagger)

> "Staggered appearance of multiple objects creates layered, cohesive
> movement and establishes visual hierarchy."

Also known as **follow-through and overlapping action** (Disney's 12
principles): different parts stop at different speeds.

## Why

Simultaneous animation of N elements reads as one heavy block. Stagger
turns the same N elements into a sequence the eye can follow — it
establishes hierarchy ("this first, then this") without any labels.

## How (GSAP)

```js
gsap.from(".grid-item", {
  y: 40,
  opacity: 0,
  duration: 0.6,
  ease: "power2.out",
  stagger: 0.08,                    // 80ms between each item
});

// Stagger from center outward:
gsap.from(".grid-item", {
  y: 40, opacity: 0, duration: 0.6,
  stagger: { each: 0.08, from: "center" },
});

// Stagger across a 2D grid (great for image walls):
gsap.from(".grid-item", {
  scale: 0.8, opacity: 0,
  stagger: { grid: [6, 6], from: "start", amount: 0.8 },
});
```

**Zajno-extracted pattern** — they normalize stagger by item count so
total duration stays bounded:

```js
const items = document.querySelectorAll(".grid-item");
gsap.from(items, {
  y: 40, opacity: 0,
  stagger: items.length > 8 ? 0.05 : 0.08,  // tighter when many items
  duration: 0.5,
});
```

## How (CSS)

```css
.grid-item { transition: transform 600ms ease-out, opacity 600ms ease-out; }
.grid-item:nth-child(1) { transition-delay: 0ms; }
.grid-item:nth-child(2) { transition-delay: 80ms; }
.grid-item:nth-child(3) { transition-delay: 160ms; }
/* … or use a CSS variable: */
.grid-item { transition-delay: calc(var(--i) * 80ms); }
```

## How (Framer Motion)

```jsx
<motion.ul
  variants={{
    visible: { transition: { staggerChildren: 0.08 } }
  }}
  initial="hidden" animate="visible"
>
  {items.map(item => (
    <motion.li key={item.id} variants={fadeUp}>{item.label}</motion.li>
  ))}
</motion.ul>
```

## Stagger timing rules

| Element count | Per-item delay | Reasoning                          |
|---------------|----------------|------------------------------------|
| 2–4           | 0.10–0.15s     | Each item feels deliberate         |
| 5–8           | 0.06–0.10s     | Sequence still readable            |
| 9–15          | 0.04–0.06s     | Cap total at ~600ms                |
| 16+           | use `amount`   | Spread total across fixed window   |

## Anti-patterns

- ❌ Staggering everything on the page — only stagger *peer* elements
- ❌ Stagger > 200ms per item — feels like loading, not animation
- ❌ Letting total stagger duration exceed ~1.2s — user gets bored
- ❌ Staggering both reveal AND hide on the same element list

See `examples/stagger-reveal.js`.
