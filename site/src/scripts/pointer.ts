/*
  One pointer, two numbers, published for the whole page.

  --pointer-x and --pointer-y live on <html>, each in -1..1, damped. Every
  cloud and every piece of art reads the same pair and multiplies by its own
  depth. One listener and one rAF for the entire site, instead of every layer
  running its own maths — and because they are custom properties, the layers
  that use them are pure CSS.

  The loop only runs while it still has somewhere to go, then stops. Nothing
  idles in the background.

  Never starts under reduced motion, and never on a device with no hover — on
  a phone there is no pointer to follow, and binding one would only cost
  battery for a parallax nobody can aim.
*/

const EASE = 0.11;

export function startPointer() {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (!matchMedia("(hover: hover) and (pointer: fine)").matches) return;

  const root = document.documentElement;
  let tx = 0,
    ty = 0,
    cx = 0,
    cy = 0,
    running = false;

  function frame() {
    cx += (tx - cx) * EASE;
    cy += (ty - cy) * EASE;
    root.style.setProperty("--pointer-x", cx.toFixed(4));
    root.style.setProperty("--pointer-y", cy.toFixed(4));
    if (Math.abs(tx - cx) > 0.0005 || Math.abs(ty - cy) > 0.0005) {
      requestAnimationFrame(frame);
    } else {
      running = false;
    }
  }

  function nudge() {
    if (!running) {
      running = true;
      requestAnimationFrame(frame);
    }
  }

  window.addEventListener(
    "pointermove",
    (e) => {
      // Read once, write once, never interleaved.
      tx = (e.clientX / window.innerWidth - 0.5) * 2;
      ty = (e.clientY / window.innerHeight - 0.5) * 2;
      nudge();
    },
    { passive: true }
  );

  window.addEventListener(
    "pointerleave",
    () => {
      tx = 0;
      ty = 0;
      nudge();
    },
    { passive: true }
  );
}
