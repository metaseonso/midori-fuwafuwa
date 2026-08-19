/*
  Inertial smooth scroll — the drift under the visitor's finger. Config is
  Zajno's production values (duration 2, ease-out expo), per the
  zajno-motion skill's extraction of their source.

  Strictly additive (crawlers-and-parallax rule): the page scrolls natively
  without this; Lenis only lerps wheel input on top of native scrolling, and
  touch scrolling stays native. Skipped entirely under reduced motion.
*/
import Lenis from "lenis";

if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  try {
    const lenis = new Lenis({
      duration: 2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      anchors: true,
    });
    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);
  } catch (e) {
    /* native scroll is the fallback — nothing to do */
  }
}
