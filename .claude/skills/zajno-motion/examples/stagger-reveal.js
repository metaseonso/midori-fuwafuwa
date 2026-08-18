// Stagger reveal — Principle 2 (Offset & Delay).
// Reveals a list / grid of items with a coherent ripple.

import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

// 1. Simple sequential stagger (rows / lists)
export function staggerReveal(selector = "[data-stagger] > *") {
  const items = gsap.utils.toArray(selector);
  if (!items.length) return;

  // Normalize stagger by count so total ≤ 800ms
  const perItem = items.length > 8 ? 0.05 : 0.08;

  gsap.from(items, {
    y: 30,
    opacity: 0,
    duration: 0.6,
    ease: "power2.out",
    stagger: perItem,
    scrollTrigger: {
      trigger: items[0],
      start: "top 85%",
      once: true,
    },
  });
}

// 2. Grid stagger — radiates from a point
export function gridReveal(selector = "[data-grid-stagger] > *", from = "center") {
  const items = gsap.utils.toArray(selector);
  if (!items.length) return;

  // Infer grid dimensions (or pass them in)
  const cols = parseInt(items[0].parentElement.dataset.cols ?? "4", 10);
  const rows = Math.ceil(items.length / cols);

  gsap.from(items, {
    scale: 0.8,
    opacity: 0,
    duration: 0.5,
    ease: "power3.out",
    stagger: {
      grid: [rows, cols],
      from,                       // "start" | "center" | "end" | "edges" | "random" | [x, y]
      amount: 0.8,                // total spread across 800ms
    },
    scrollTrigger: {
      trigger: items[0].parentElement,
      start: "top 80%",
      once: true,
    },
  });
}

// HTML usage:
//
// <ul data-stagger>
//   <li>One</li>
//   <li>Two</li>
//   <li>Three</li>
// </ul>
//
// <div data-grid-stagger data-cols="4">
//   <div class="tile">…</div>  (16 tiles)
//   …
// </div>
