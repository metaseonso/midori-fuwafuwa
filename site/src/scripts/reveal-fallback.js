/*
  Progressive-enhancement fallback for browsers that run JS but don't support
  animation-timeline: view() yet. Where the CSS scroll-driven reveal in
  global.css is supported, this script does nothing — the compositor handles
  it. Where it isn't, this uses IntersectionObserver to add .is-visible.
  Any failure here defaults to showing everything, never hiding it.
*/
try {
  const supportsScrollTimeline =
    typeof CSS !== "undefined" && CSS.supports && CSS.supports("animation-timeline: view()");

  const reveals = document.querySelectorAll(".reveal");

  if (!supportsScrollTimeline && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        }
      },
      { rootMargin: "0px 0px -10% 0px", threshold: 0.15 }
    );
    reveals.forEach((el) => io.observe(el));
  } else if (!supportsScrollTimeline) {
    reveals.forEach((el) => el.classList.add("is-visible"));
  }
} catch (e) {
  document.querySelectorAll(".reveal").forEach((el) => el.classList.add("is-visible"));
}
