/*
  Inertial smooth scroll — the drift under the visitor's finger.

  duration was 2. That is a two-second glide after every wheel tick, and with
  scroll-driven parallax hanging off it the whole world kept sliding long after
  the visitor stopped. Frame timing was a clean 60fps throughout — the problem
  was never dropped frames, it was latency. 0.85 still reads as unhurried and
  gives the input back.

  Strictly additive (crawlers-and-parallax rule): the page scrolls natively
  without this; Lenis only lerps wheel input on top of native scrolling, and
  touch scrolling stays native. Skipped entirely under reduced motion.
*/
import Lenis from "lenis";

if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  try {
    const lenis = new Lenis({
      duration: 0.85,
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
