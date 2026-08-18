// Lenis smooth-scroll wired to GSAP ScrollTrigger.
// Config values extracted from cdn.zajno.com/dev/motion/script.v33.min.js
//
// Install: npm i @studio-freight/lenis gsap

import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "@studio-freight/lenis";

gsap.registerPlugin(ScrollTrigger);

// Skip smooth scroll on mobile (Zajno does too — performance + native UX).
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i
  .test(navigator.userAgent);

if (!isMobile) {
  const lenis = new Lenis({
    duration: 2,
    easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  });

  // Bridge Lenis -> ScrollTrigger
  lenis.on("scroll", ScrollTrigger.update);
  gsap.ticker.add(time => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);

  // Expose for debugging if needed
  window.__lenis = lenis;
}
