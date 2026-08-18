// Dimension — Principle 6.
// Pointer-driven 3D tilt on a layered card.
// Each child with data-depth moves more aggressively the higher its depth.

import { gsap } from "gsap";

export function setupDimensionCard(selector = ".dim-card") {
  document.querySelectorAll(selector).forEach(card => {
    // Respect user preference
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    // Mobile: skip (too jittery on touch, drains battery)
    if (window.innerWidth <= 768) return;

    const layers = card.querySelectorAll("[data-depth]");

    // Persist perspective + 3D context
    gsap.set(card, { transformPerspective: 1000, transformStyle: "preserve-3d" });

    let rafId = null;
    let targetX = 0, targetY = 0;

    function onMove(e) {
      const rect = card.getBoundingClientRect();
      targetX = (e.clientX - rect.left) / rect.width  - 0.5;
      targetY = (e.clientY - rect.top)  / rect.height - 0.5;

      if (rafId) return;
      rafId = requestAnimationFrame(apply);
    }

    function apply() {
      rafId = null;

      gsap.to(card, {
        rotateY:  targetX * 8,                 // max ±8°
        rotateX: -targetY * 8,
        duration: 0.4,
        ease: "power2.out",
      });

      layers.forEach(layer => {
        const depth = parseFloat(layer.dataset.depth) || 0;
        gsap.to(layer, {
          x: targetX * 40 * depth,
          y: targetY * 40 * depth,
          duration: 0.4,
          ease: "power2.out",
        });
      });
    }

    function onLeave() {
      gsap.to(card,   { rotateX: 0, rotateY: 0, duration: 0.6, ease: "power3.out" });
      gsap.to(layers, { x: 0, y: 0,              duration: 0.6, ease: "power3.out" });
    }

    card.addEventListener("mousemove", onMove);
    card.addEventListener("mouseleave", onLeave);
  });
}

// HTML usage:
//
// <div class="dim-card">
//   <div data-depth="0.2"><img src="bg.jpg"  /></div>
//   <div data-depth="0.5"><img src="mid.png" /></div>
//   <div data-depth="1.0"><h2>Foreground</h2></div>
// </div>
//
// CSS:
// .dim-card { position: relative; will-change: transform; }
// .dim-card > [data-depth] { position: absolute; inset: 0; will-change: transform; }
