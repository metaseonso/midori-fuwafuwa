// Fade + transform — Principle 3.
// Never fade alone. Always pair with y, scale, or blur.

import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

// Workhorse: fade + slide up
export function fadeUp(selector = "[data-fade-up]") {
  document.querySelectorAll(selector).forEach(el => {
    gsap.from(el, {
      y: 30,
      opacity: 0,
      duration: 0.6,
      ease: "power2.out",
      scrollTrigger: { trigger: el, start: "top 85%", once: true },
    });
  });
}

// Card: fade + scale
export function fadeScale(selector = "[data-fade-scale]") {
  document.querySelectorAll(selector).forEach(el => {
    gsap.from(el, {
      scale: 0.92,
      opacity: 0,
      duration: 0.5,
      ease: "power3.out",
      scrollTrigger: { trigger: el, start: "top 85%", once: true },
    });
  });
}

// Premium: fade + blur (GPU-heavy — use sparingly, ideally on hero only)
export function fadeBlur(selector = "[data-fade-blur]") {
  document.querySelectorAll(selector).forEach(el => {
    gsap.from(el, {
      opacity: 0,
      filter: "blur(20px)",
      duration: 0.8,
      ease: "power2.out",
      scrollTrigger: { trigger: el, start: "top 85%", once: true },
    });
  });
}

// Respect prefers-reduced-motion — disable all of the above
export function respectReducedMotion() {
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (prefersReduced) {
    // Make everything immediately visible
    document.querySelectorAll("[data-fade-up], [data-fade-scale], [data-fade-blur]")
      .forEach(el => { el.style.opacity = 1; el.style.transform = "none"; el.style.filter = "none"; });
    return true;
  }
  return false;
}
