// Morph + Mask — Principles 4 and 5 combined.
//
// Pattern A: hamburger ↔ X (transform morph, same DOM node)
// Pattern B: clip-path reveal (mask)
// Pattern C: FLIP shared-element morph (card → detail view)

import { gsap } from "gsap";
import { Flip } from "gsap/Flip";

gsap.registerPlugin(Flip);

// ─── Pattern A: hamburger ↔ X ──────────────────────────────────────────
export function toggleHamburger(btn) {
  const isOpen = btn.classList.toggle("is-open");
  const top    = btn.querySelector(".bar-top");
  const mid    = btn.querySelector(".bar-mid");
  const bot    = btn.querySelector(".bar-bot");

  if (isOpen) {
    gsap.to(top, { y: 8,  rotate: 45,  duration: 0.3, ease: "power3.inOut" });
    gsap.to(mid, { opacity: 0,         duration: 0.2 });
    gsap.to(bot, { y: -8, rotate: -45, duration: 0.3, ease: "power3.inOut" });
  } else {
    gsap.to(top, { y: 0, rotate: 0, duration: 0.3, ease: "power3.inOut" });
    gsap.to(mid, { opacity: 1,      duration: 0.3 });
    gsap.to(bot, { y: 0, rotate: 0, duration: 0.3, ease: "power3.inOut" });
  }
}

// ─── Pattern B: clip-path mask reveal ───────────────────────────────────
export function maskReveal(el, direction = "right") {
  const dirs = {
    right:  { from: "inset(0 100% 0 0)", to: "inset(0 0 0 0)" },
    left:   { from: "inset(0 0 0 100%)", to: "inset(0 0 0 0)" },
    up:     { from: "inset(0 0 100% 0)", to: "inset(0 0 0 0)" },
    down:   { from: "inset(100% 0 0 0)", to: "inset(0 0 0 0)" },
    circle: { from: "circle(0% at 50% 50%)", to: "circle(100% at 50% 50%)" },
  };
  const { from, to } = dirs[direction] || dirs.right;

  gsap.fromTo(el,
    { clipPath: from },
    { clipPath: to, duration: 0.8, ease: "power3.out" }
  );
}

// ─── Pattern C: FLIP shared-element morph ──────────────────────────────
// Captures the current layout of `el`, runs `mutate()` to change the DOM,
// then animates from the old layout to the new one.
export function morphTo(el, mutate, opts = {}) {
  const state = Flip.getState(el);
  mutate();
  return Flip.from(state, {
    duration: opts.duration ?? 0.6,
    ease: opts.ease ?? "power3.inOut",
    scale: true,                       // scale, don't resize
    absolute: true,                    // promote to position:absolute mid-flight
    ...opts,
  });
}

// Usage:
//
// card.addEventListener("click", () => {
//   morphTo(card, () => {
//     card.classList.toggle("is-expanded");      // CSS controls width/height
//   });
// });
