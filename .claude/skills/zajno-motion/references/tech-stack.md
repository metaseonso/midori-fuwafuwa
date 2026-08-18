# Tech Stack — what Zajno actually uses

Extracted from `motion.zajno.com` page source on 2026-05-23.

| Library              | Version  | Role                                      |
|----------------------|----------|-------------------------------------------|
| **GSAP**             | 3.10.4   | Timeline + tween engine                   |
| **GSAP ScrollTrigger** | 3.10.4 | Scroll-bound animations                   |
| **GSAP CustomEase**  | 3.10.4   | Custom cubic-bezier curves                |
| **GSAP MotionPath**  | 3.11.4   | Animate along an SVG path                 |
| **GSAP Observer**    | 3.11.4   | Unified pointer / wheel / touch events    |
| **Lenis**            | latest   | Smooth scroll                             |
| **Lottie**           | (impl)   | Vector animation playback (`.json` files) |
| **Matter.js**        | 0.18.0   | 2D physics (for one interactive section)  |
| **Splide**           | 2.4.21   | Carousel slider                           |

## Install (modern bundler — Vite / Next / Webpack)

```bash
npm i gsap @studio-freight/lenis lottie-web matter-js @splidejs/splide
```

```js
// Register GSAP plugins once at app entry:
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { CustomEase }    from "gsap/CustomEase";
import { Observer }      from "gsap/Observer";

gsap.registerPlugin(ScrollTrigger, CustomEase, Observer);
```

## CDN (vanilla HTML)

Zajno loads from CDNJS — copy this if you're building a static page:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.10.4/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.10.4/ScrollTrigger.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.10.4/CustomEase.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.4/Observer.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.4/MotionPathPlugin.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/studio-freight/lenis@latest/bundled/lenis.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.18.0/matter.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lottie-web@5/build/player/lottie.min.js"></script>
```

## Lottie — for hero / illustrative animation

Zajno uses a Lottie file per principle (~30 `.json` files on the page).
This is how *each principle's hero illustration* is animated. Lottie
exports After Effects animations to a JSON timeline the browser plays.

```js
import lottie from "lottie-web";

const anim = lottie.loadAnimation({
  container: document.querySelector("#hero-anim"),
  renderer:  "svg",                  // svg | canvas | html
  loop:      false,
  autoplay:  false,
  path:      "/anim/hero.json",
});

// Drive it with scroll:
ScrollTrigger.create({
  trigger: "#hero",
  start: "top top",
  end: "bottom top",
  scrub: 1,
  onUpdate: self => anim.goToAndStop(anim.totalFrames * self.progress, true),
});
```

To produce the Lottie files: After Effects + Bodymovin plugin
(or Lottielab for a designer-friendly web tool).

## Why this stack?

- **GSAP** has the best timeline API in the JS ecosystem — `.timeline()`
  with `.to() .from() .fromTo() .add()` lets you compose complex
  choreography readably.
- **ScrollTrigger** + **Lenis** is the modern smooth-parallax combo;
  without Lenis, parallax stutters on trackpads.
- **Lottie** lets a *designer* author the animation in After Effects
  rather than a developer writing keyframes by hand. This is the
  secret to studio-quality hero animations.
- **Matter.js** is overkill unless you need real physics (Zajno uses it
  for one section). For "wobble" or "bounce", use CustomEase instead.

## Performance budget

- Lenis adds ~10kb gzipped, GSAP+ScrollTrigger ~30kb, Lottie ~60kb
- Lottie `.json` files are 5–80kb each — lazy-load them per-viewport
- Use `ScrollTrigger.create({ once: true })` for reveals — releases the
  trigger after firing once, frees memory
- On mobile (`< 992px` is Zajno's breakpoint), simplify or disable
  parallax/dimension; they observed perf wins from skipping these.
