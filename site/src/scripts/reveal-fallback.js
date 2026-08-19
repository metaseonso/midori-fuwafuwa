/*
  Correctness backstop for .reveal elements, in three layers:
  1. CSS animation-timeline: view() in global.css is the primary mechanism —
     smooth native reveal during normal scrolling, where supported.
  2. IntersectionObserver here catches anything the CSS path misses — it has
     been observed to leave elements stuck at opacity:0 when the viewport is
     much taller than the page (a crawler expanding its viewport to the full
     page height and never scrolling reproduces this reliably).
  3. A short timeout force-reveals anything still hidden, in case neither of
     the above ran for some reason (e.g. a backgrounded/non-rendered tab).
  Nothing should ever stay invisible because one mechanism failed.
*/
try {
  const reveals = document.querySelectorAll(".reveal");

  const reveal = (el) => {
    el.classList.add("is-visible");
    // A stuck/degenerate scroll-timeline animation can keep controlling
    // opacity even after .is-visible sets it via a transition — animations
    // override the normal cascade for the properties they animate. Killing
    // the animation outright removes that conflict.
    el.style.animation = "none";
  };

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            reveal(entry.target);
            io.unobserve(entry.target);
          }
        }
      },
      { rootMargin: "0px 0px -10% 0px", threshold: 0.15 }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach(reveal);
  }

  setTimeout(() => {
    reveals.forEach((el) => {
      if (parseFloat(getComputedStyle(el).opacity) < 0.99) reveal(el);
    });
  }, 1500);
} catch (e) {
  document.querySelectorAll(".reveal").forEach((el) => {
    el.classList.add("is-visible");
    el.style.animation = "none";
  });
}
