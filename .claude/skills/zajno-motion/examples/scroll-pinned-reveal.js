// Scroll-pinned reveal — the "hero zooms out as you scroll" pattern.
// Combines Principle 7 (Parallax) and Principle 8 (Zoom).
//
// Zajno-extracted options:
//   pin: true, anticipatePin: 1, scrub: 1
// (the `anticipatePin: 1` prevents pin-flicker at section boundaries)

import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function setupPinnedHeroReveal(sectionSelector = ".hero-pinned") {
  const section = document.querySelector(sectionSelector);
  if (!section) return;

  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: section,
      start: "top top",
      end: () => "+=" + window.innerHeight,
      pin: true,
      anticipatePin: 1,
      scrub: 1,
    },
  });

  // Camera pulls back — image starts zoomed in, returns to normal
  tl.fromTo(section.querySelector(".hero-img"),
    { scale: 2.5 },
    { scale: 1, ease: "none" },
    0
  );

  // Headline fades + rises in over the same scroll range
  tl.fromTo(section.querySelector(".hero-title"),
    { y: 80, opacity: 0 },
    { y: 0,  opacity: 1, ease: "none" },
    0.3                   // start at 30% through the pinned scroll
  );

  // Subtitle follows
  tl.fromTo(section.querySelector(".hero-sub"),
    { y: 40, opacity: 0 },
    { y: 0,  opacity: 1, ease: "none" },
    0.5
  );

  return tl;
}

// HTML structure expected:
//
// <section class="hero-pinned">
//   <img class="hero-img" src="..." />
//   <h1 class="hero-title">…</h1>
//   <p  class="hero-sub">…</p>
// </section>
