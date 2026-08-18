# Principle 7 — Parallax

> "Multiple layered objects move simultaneously along x and y axes;
> farther objects move less, creating spatial illusion."

## Why

Parallax is dimension applied to scroll. Foreground elements slide
faster than background elements as the page scrolls, exactly like
looking out a moving car window. It is the cheapest, most effective way
to make a flat page feel three-dimensional.

## How (GSAP ScrollTrigger, the gold standard)

```js
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

document.querySelectorAll("[data-parallax]").forEach(el => {
  const speed = parseFloat(el.dataset.parallax); // e.g. 0.3 = slow, 0.8 = fast
  gsap.to(el, {
    yPercent: -100 * speed,
    ease: "none",                     // linear is correct here — driven by scrub
    scrollTrigger: {
      trigger: el,
      start: "top bottom",            // when top of element hits bottom of viewport
      end:   "bottom top",            // until bottom of element passes top of viewport
      scrub: true,                    // bind progress to scroll
    },
  });
});
```

```html
<section class="hero">
  <img src="sky.jpg"      data-parallax="0.2" />  <!-- moves slowest = farthest -->
  <img src="mountains.png" data-parallax="0.5" />
  <img src="trees.png"     data-parallax="0.8" />
  <h1                      data-parallax="1.0">Headline</h1>
</section>
```

## Smooth-scroll layer — Lenis (what Zajno actually uses)

Native scroll is *jittery* on parallax. Zajno wraps scrolling in
[Lenis](https://github.com/darkroomengineering/lenis):

```js
import Lenis from "@studio-freight/lenis";

// Zajno's actual config (extracted from script.v33.min.js):
const lenis = new Lenis({
  duration: 2,
  easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)),  // ease-out expo
});

function raf(time) { lenis.raf(time); requestAnimationFrame(raf); }
requestAnimationFrame(raf);

// Tell ScrollTrigger to use Lenis:
lenis.on("scroll", ScrollTrigger.update);
gsap.ticker.add(time => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);
```

See `examples/lenis-smooth-scroll.js` — that's the full integration.

## Parallax speed scale

| `data-parallax` | Visual depth        | Use for                  |
|-----------------|---------------------|--------------------------|
| `0.1 – 0.3`     | Background / sky    | Large, blurred imagery   |
| `0.4 – 0.6`     | Mid-ground          | Decorative shapes        |
| `0.7 – 0.9`     | Foreground          | Text overlay, characters |
| `1.0` (none)    | Pinned to scroll    | Headlines, CTA           |
| `> 1.0`         | Faster than scroll  | Tickers, marquee text    |

## Anti-patterns

- ❌ Parallax on mobile by default — disable below ~768px (drains battery,
   feels weird on small viewports). At minimum, halve the offset.
- ❌ Parallax + sticky positioning — they fight. Pick one.
- ❌ More than 3–4 parallax layers per section — diminishing returns.
- ❌ Parallax without `scrub: true` — defeats the point.
- ❌ Forgetting `ease: "none"` — eased parallax oscillates after scroll stops.
- ❌ Heavy `<img>` elements parallaxed without `will-change: transform`.

See `examples/parallax-layers.js`.
