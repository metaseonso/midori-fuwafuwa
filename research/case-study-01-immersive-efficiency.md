---
title: "Case Study 01 — Efficient Immersive Showcase"
subtitle: "What the fastest, most beautiful production-studio sites actually do — and the fusion that fits Midori Fuwafuwa"
date: 2026-08-18
status: research → conclusion
---

# Case Study 01 — Efficient Immersive Showcase

## The question

Two things are usually in tension on a studio site: making it feel alive (motion, depth, a world you scroll *into*) and making it feel fast (nothing chugs, nothing waits, nothing punishes a mid-range phone). This case study asks what the current best techniques are for getting both at once, then looks at what actually-good production-studio sites choose to *say* to a visitor, so the two can be fused into one recommendation for Midori Fuwafuwa.

---

## Part A — The efficient side: beautiful motion that costs almost nothing

The pattern across every current best-practice source is the same one, repeated at every layer: **push work onto the browser's compositor, and off the main thread.** Everything below is really one idea applied five times.

**The scroll engine layer — increasingly, it's free.**
CSS now has native scroll-driven animation (`animation-timeline: scroll()` / `view()`, with `animation-range` to control entry/exit). Because it only ever touches `transform` and `opacity`, it runs on the compositor thread, completely decoupled from whatever the main thread is doing — Chrome's own case study shows the JS-listener equivalent turning janky under load while the CSS version stays smooth. No `requestAnimationFrame` loop, no scroll-event throttling, no `getBoundingClientRect()` polling. Support is now solid in Chrome/Edge and Safari 26; Firefox lags, so the honest move is `@supports (animation-timeline: scroll())` with a static or CSS-transition fallback — not a JS polyfill, which would cancel out the whole performance win. Alongside it, the **View Transitions API** lets a plain, cheap multi-page site *feel* like an app with smooth page-to-page morphs, without shipping a client-side router at all.

**Where JS scroll libraries are still worth it — but leaner than they used to be.**
For scroll-linked choreography beyond what pure CSS timelines can express (staggered reveals, pinned sections, scrubbed sequences), the field has converged on one small stack: **Lenis** (~4KB) for smoothing native scroll input without hijacking the scrollbar — the way older libraries like Locomotive Scroll used to, at real cost to accessibility and feel — paired with **GSAP ScrollTrigger** for choreography. GSAP's own performance guidance is blunt: animate only `transform`/`opacity`, apply `will-change` only to elements actively animating, use `ScrollTrigger.batch()` instead of per-element triggers, tune `scrub` with a numeric lag rather than binding 1:1 to raw scroll, and read-then-write DOM values in that order, never interleaved (interleaving is what causes layout thrashing).

**The dimensional layer — used sparingly, loaded lazily.**
Full WebGL/Three.js scenes are the most expensive tool in the kit, so the efficient sites treat them as a *seasoning*, not the whole meal: mount the canvas only when it scrolls into view (`IntersectionObserver`), use React Three Fiber's `frameloop="demand"` so it renders on change rather than a continuous 60fps loop, and drop pixel ratio/post-processing during interaction and restore it at idle (Drei's `PerformanceMonitor`/`regress()`). Where geometry and textures are unavoidable, compress them — Draco/meshopt cut mesh size 90%+, KTX2/Basis textures stay GPU-compressed instead of ballooning 10x in VRAM the way a raw PNG does. WebGPU is now baseline across major browsers and Three.js r171+ can swap renderers with automatic WebGL2 fallback, but it's still best treated as a progressive enhancement, not a requirement.

**Asset discipline is half the battle before any animation code runs at all.**
AVIF/WebP for photographic assets; flat-color, sharp-edge illustration (exactly the chibi style Midori Fuwafuwa already draws in) often compresses *better* as optimized SVG/PNG-8 than as a lossy photographic format, so the format choice should follow the art style, not a blanket rule. Native `loading="lazy"` now covers most below-the-fold image cases without a JS library. Fonts: WOFF2 only, subset aggressively, and mix `font-display` strategy per asset — `swap` where the brand font matters, `optional` where a layout shift would hurt more than a font substitution would.

**Accessibility and efficiency are the same path, not a trade-off.**
`prefers-reduced-motion: reduce` should gate whether a WebGL canvas or parallax scene *initializes at all* — not just whether it animates. That means the cheapest possible render path and the most accessible one are the same code path: skip the asset download, skip the GPU cost, skip the scene graph, for anyone who has asked for less motion. Building the reduced-motion state first, as the baseline, and layering richness on top for everyone else, is both the accessible default and the fastest possible page.

---

## Part B — What the best studio sites actually put in front of a visitor

Looking across a spread of standout studios (Immersive Garden, basement.studio, ToyFight, Cuberto, Locomotive, Active Theory, Bruno Simon, and the current wave of Three.js showcase sites), a few real patterns repeat — not just "looks impressive," but structurally, *what content earns its place*:

- **Content depth is a positioning choice, tied to who's expected to read it — not a universal "more is better."** Studios pitching ultra-luxury brand clients (Immersive Garden) show almost no process or team content; the portfolio *is* the pitch, and explaining it would undercut the mystique. Studios courting technically literate clients or hires (Active Theory, basement.studio) publish deep engineering write-ups as a *separate* channel. Studios courting a broad agency-shopping audience (Cuberto) front-load an FAQ that pre-empts the sales call. None of these are "more transparent = better" — they're calibrated to the audience.
- **"Behind the scenes" is consistently its own destination, not a tab on the project page.** Active Theory's technical case studies live on a separate Medium publication; basement.studio has a dedicated "Lab"; Bruno Simon has a "Behind the Scene" credits page. Process content earns more trust living apart from the polished result, not folded into it.
- **When a studio has an actual character or playful core concept, the site performs the personality instead of describing it.** ToyFight's answering-machine easter egg, Rive's cursor-reactive character animation, Bruno Simon's drivable-car navigation — in each case the interaction itself *is* the demonstration of craft. This is the single most relevant pattern for a studio whose whole identity is two chibi mascot-characters.
- **At small scale, value shifts from breadth to depth of relationship.** A two-person operation can't out-produce a fifty-person agency's project count, and Bruno Simon (the closest structural analog in this research — a small, personality-forward, technically transparent operation) doesn't try to. Instead it adds return-visit hooks: credits, an open-source trail, a community space. The lesson for a small studio isn't "show more work," it's "give people a reason to come back."
- **Organizing a small number of distinct projects as separate spatial "worlds" or "rooms" — rather than one continuous grid — recurs at the high end** (Cartier's six self-contained 3D rooms, each product entered and exited on scroll) and maps unusually well onto a studio whose founding premise is literally a shared Dreamland — here, that becomes the **Field** (see Conclusion): one open, explorable space per production, instead of a room in a hallway.

---

## Conclusion — the fusion: efficient Fields in the Dreamland

Put the two halves together, and the shape that falls out isn't "add a 3D hero" or "add more case studies" — it's a **specific, small, coherent idea**: treat the site itself as a layered-parallax diorama of the Dreamland, where each production is its own open **Field** you wander into, and let the mascots — not copy — carry the personality.

*(Naming note: "room" from the earlier draft is retired in favor of **Field** — an open, walkable, pastoral space rather than a boxed-in room, truer to "Field of Dreams" and to a Dreamland setting. See the reference README for how Field pairs with the companion term **Forest**, introduced for Case Study 02's living layer.)*

Concretely, for Midori Fuwafuwa:

1. **Build the home experience as 2D/2.5D layered parallax, not full 3D.** The chibi/flat-illustration style is already the *efficient* choice — layered PNG/SVG art parallaxing at different scroll speeds (driven by native CSS scroll-timelines where supported, Lenis + GSAP where finer control is needed) reads as rich and dreamlike while staying compositor-cheap. Reserve WebGL for a single, deliberate accent — a soft glow/particle shimmer echoing the sparkle-and-spiral motifs already in Seonso's key art — lazy-mounted, `frameloop="demand"`, and skipped entirely under `prefers-reduced-motion`.
2. **Structure productions as Fields in the Dreamland, not tiles in a grid.** Each production/pipeline gets its own small scrollable open space — its own palette accent, its own mascot pose — entered from a central map/hub. This is the Cartier "six rooms" pattern, re-skinned as open Fields and scaled down to two founders and a handful of productions — a natural narrative fit for "Seonso and Grumpy Carrot share this Dreamland."
3. **Let the mascots perform the studio's personality instead of a copy deck explaining it.** A small guided interaction — the cloud mascot painting something new when a section loads, Grumpy Carrot's chaos-energy micro-animations on hover, Seonso's calm spiral motif as a loading/transition state — does the positioning work that an "About us" paragraph can't.
4. **Keep the chrome minimal and let mystique carry weight, the way Immersive Garden does** — but reserve a *separate* "behind the scenes" / studio-journal destination for process and technical transparency, rather than explaining everything on the front page. That separate destination is exactly what Case Study 02 solves — it's the **Forest** at the edge of each Field: the living, auto-updating pipeline recap, so the same restraint that makes the front page feel calm and minimal also makes it low-maintenance.
5. **Design the reduced-motion state first.** For this brand, that's not a compromise — a static, softly-lit diorama frame of each Dreamland Field, mascots in their resting poses, is *already* a beautiful outcome, and it means the accessible path and the fast path are the same path.

This is the fusion: efficiency isn't a constraint fighting the immersive goal here, because the art style Midori Fuwafuwa already draws in — flat, chibi, hand-illustrated — is inherently one of the cheapest things to render beautifully. The novel part isn't a technique; it's treating the studio's own Dreamland premise as the site's literal information architecture.

---

## Sources

**Efficient motion & rendering**
- [MDN — Scroll-driven animation timelines](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations/Timelines)
- [Chrome for Developers — A case study on scroll-driven animations performance](https://developer.chrome.com/blog/scroll-animation-performance-case-study)
- [Chrome for Developers — View transitions case studies](https://developer.chrome.com/blog/css-ui-ecommerce-vt)
- [Smashing Magazine — An Introduction to CSS Scroll-Driven Animations](https://www.smashingmagazine.com/2024/12/introduction-css-scroll-driven-animations/)
- [Lenis — official site](https://lenis.dev/) · [darkroomengineering/lenis](https://github.com/darkroomengineering/lenis)
- [GSAP — gsap-scrolltrigger SKILL.md (GreenSock)](https://github.com/greensock/gsap-skills/blob/main/skills/gsap-scrolltrigger/SKILL.md) · [gsap-performance SKILL.md](https://github.com/greensock/gsap-skills/blob/main/skills/gsap-performance/SKILL.md)
- [React Three Fiber — Scaling Performance](https://r3f.docs.pmnd.rs/advanced/scaling-performance)
- [Three.js docs — KTX2Loader](https://threejs.org/docs/pages/KTX2Loader.html) · [DRACOLoader](https://threejs.org/docs/pages/DRACOLoader.html)
- [web.dev — WebGPU is now supported in major browsers](https://web.dev/blog/webgpu-supported-major-browsers)
- [web.dev — Best practices for fonts](https://web.dev/articles/font-best-practices)
- [MDN — prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion)

**Studio showcases**
- [Immersive Garden](https://immersive-g.com/)
- [basement.studio](https://basement.studio/) · [Codrops — Inside the Studio Powering the Internet's Boldest Brands](https://tympanus.net/codrops/2025/12/15/from-basement-to-breakthroughs-inside-the-studio-powering-the-internets-boldest-brands/)
- [Codrops — Case Study: ToyFight 2024](https://tympanus.net/codrops/2024/06/11/case-study-toyfight-2024/)
- [Cuberto](https://cuberto.com/)
- [Locomotive](https://locomotive.ca/en)
- [Active Theory — Case Studies (Medium)](https://medium.com/active-theory) · [The Story of Technology Built at Active Theory](https://medium.com/active-theory/the-story-of-technology-built-at-active-theory-5d17ae0e3fb4)
- [Bruno Simon](https://bruno-simon.com/)
- [Utsubo — Best Three.js Websites 2026](https://www.utsubo.com/blog/best-threejs-websites-2026)

*(Full annotated source list with per-technique notes available in the research transcript for this session — this file keeps only the primary references.)*
