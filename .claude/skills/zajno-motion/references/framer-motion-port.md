# Framer Motion / React port

The principles are framework-agnostic. Here's how to translate the
GSAP-flavored examples to Framer Motion (the dominant React lib).

## Easing translation

```js
// GSAP                              // Framer Motion
ease: "power2.out"                   transition={{ ease: [0.25, 1, 0.5, 1] }}
ease: "power3.out"                   transition={{ ease: [0.33, 1, 0.68, 1] }}
ease: "power4.out"                   transition={{ ease: [0.16, 1, 0.3, 1] }}
ease: "power3.inOut"                 transition={{ ease: [0.65, 0, 0.35, 1] }}
ease: "expo.out"                     transition={{ ease: [0.16, 1, 0.3, 1] }}

// Zajno's "bounce" — Framer takes the same bezier control points:
ease: "bounce" (custom)              transition={{ type: "spring", bounce: 0.4 }}
                                     // — or use the literal bezier with type:"tween"
```

## Principle ports

### 1. Easing
```jsx
<motion.div
  initial={{ y: 30, opacity: 0 }}
  animate={{ y: 0, opacity: 1 }}
  transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
/>
```

### 2. Offset & Delay (stagger)
```jsx
const list = {
  visible: { transition: { staggerChildren: 0.08, delayChildren: 0.1 } }
};
const item = {
  hidden: { y: 30, opacity: 0 },
  visible: { y: 0, opacity: 1, transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] } }
};

<motion.ul variants={list} initial="hidden" animate="visible">
  {items.map(i => <motion.li key={i.id} variants={item}>{i.label}</motion.li>)}
</motion.ul>
```

### 3. Fade with transform
```jsx
<motion.div
  initial={{ opacity: 0, y: 30 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-10%" }}
  transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
/>
```

### 4. Morph (shared layout)
Framer's `layoutId` does the FLIP morph for you:
```jsx
{!expanded && (
  <motion.div layoutId="card" onClick={() => setExpanded(true)}>...</motion.div>
)}
{expanded && (
  <motion.div layoutId="card" onClick={() => setExpanded(false)}>...</motion.div>
)}
```

### 5. Masking (clip-path)
Framer doesn't animate `clipPath` natively as smoothly as GSAP, but:
```jsx
<motion.div
  initial={{ clipPath: "inset(0 100% 0 0)" }}
  animate={{ clipPath: "inset(0 0 0 0)" }}
  transition={{ duration: 0.8, ease: [0.83, 0, 0.17, 1] }}
/>
```

### 6. Dimension (tilt)
```jsx
import { useMotionValue, useTransform } from "framer-motion";

function TiltCard() {
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const rotateY = useTransform(x, [-0.5, 0.5], [-8, 8]);
  const rotateX = useTransform(y, [-0.5, 0.5], [8, -8]);

  return (
    <motion.div
      onPointerMove={e => {
        const r = e.currentTarget.getBoundingClientRect();
        x.set((e.clientX - r.left) / r.width - 0.5);
        y.set((e.clientY - r.top)  / r.height - 0.5);
      }}
      onPointerLeave={() => { x.set(0); y.set(0); }}
      style={{ rotateX, rotateY, transformPerspective: 1000 }}
    />
  );
}
```

### 7. Parallax
Use `useScroll` + `useTransform`:
```jsx
import { useScroll, useTransform } from "framer-motion";

function ParallaxLayer({ speed = 0.5, children }) {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], ["0%", `${-100 * speed}%`]);
  return <motion.div style={{ y }}>{children}</motion.div>;
}
```

For smooth scroll behind Framer Motion, layer Lenis on top — they
coexist fine.

### 8. Zoom (scroll-pinned)
Framer doesn't pin natively. For pinned scroll-zooms, use Lenis +
GSAP ScrollTrigger alongside Framer Motion (they don't conflict).

## When NOT to use Framer Motion

- You need ScrollTrigger pinning → use GSAP
- You need SVG path morphing → use GSAP MorphSVG or flubber
- You need a coordinated timeline across 10+ elements → GSAP's `gsap.timeline()`
  is more readable than chained `useEffect`s

Otherwise, Framer Motion is the right choice for any React app.
