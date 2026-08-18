// Zajno's actual custom cubic-bezier curves — lifted VERBATIM from their
// production source on 2026-05-23.
//
// Register once at app entry. Then use ease: "bounce" or ease: "bounceSmall".

import { gsap } from "gsap";
import { CustomEase } from "gsap/CustomEase";

gsap.registerPlugin(CustomEase);

// Two-bump bounce — overshoots strongly, recovers, settles.
// Use for: logo accents, hero CTA "pulse" moments.
CustomEase.create(
  "bounce",
  "M0,0 C0.05222,-0.59802 0.31828,-1.38625 0.55039,0 0.65208,-0.78892 0.94566,-0.58262 1,1"
);

// Single-bump bounce — subtler.
// Use for: hover-state confirmations, micro-interactions.
CustomEase.create(
  "bounceSmall",
  "M0,0,C0.052,-0.598,0.246,-0.72,0.336,0,0.498,-0.502,0.792,-0.482,1,1"
);

// Bonus: ease-out exponential (same shape as Lenis scroll easing).
// Use for: long-distance hero entrances.
CustomEase.create(
  "expoOut",
  "M0,0 C0.16,1 0.3,1 1,1"
);

// Example usage:
//
// gsap.from(".cta", { scale: 0, duration: 0.6, ease: "bounce" });
// gsap.to(".badge", { y: -4, duration: 0.3, ease: "bounceSmall", yoyo: true, repeat: 1 });
// gsap.from(".hero-title", { y: 80, opacity: 0, duration: 1, ease: "expoOut" });
