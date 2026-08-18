// Parallax layers — Principle 7.
// Each layer moves at a different rate via data-parallax="<speed>".

import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function setupParallax(selector = "[data-parallax]") {
  // Bail on mobile — parallax is desktop-only at Zajno
  if (window.innerWidth <= 991) return;

  document.querySelectorAll(selector).forEach(el => {
    const speed = parseFloat(el.dataset.parallax);
    if (isNaN(speed)) return;

    gsap.to(el, {
      yPercent: -100 * speed,
      ease: "none",                    // linear — scrub provides the curve
      scrollTrigger: {
        trigger: el,
        start: "top bottom",
        end: "bottom top",
        scrub: true,
      },
    });
  });
}

// Horizontal-axis variant (for "sliding ribbons" common in hero sections):
export function setupParallaxX(selector = "[data-parallax-x]") {
  if (window.innerWidth <= 991) return;

  document.querySelectorAll(selector).forEach(el => {
    const speed = parseFloat(el.dataset.parallaxX);
    if (isNaN(speed)) return;

    gsap.to(el, {
      xPercent: -100 * speed,
      ease: "none",
      scrollTrigger: {
        trigger: el,
        start: "top bottom",
        end: "bottom top",
        scrub: true,
      },
    });
  });
}

// HTML usage:
//
// <section class="hero">
//   <img src="sky.jpg"       data-parallax="0.2" />
//   <img src="mountains.png" data-parallax="0.5" />
//   <img src="trees.png"     data-parallax="0.8" />
//   <h1>Headline</h1>
// </section>
