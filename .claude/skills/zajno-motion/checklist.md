# Quality Gate — "Does it feel like Zajno?"

Run through this before declaring a motion implementation done.

## Easing (Principle 1)

- [ ] No `transition: linear` anywhere except scrub-driven scroll
- [ ] Page uses ≤ 3 distinct eases total
- [ ] Entering elements use ease-out family (`power2.out` / `power4.out`)
- [ ] Exiting elements use ease-in family
- [ ] Morphs/zooms use ease-in-out (`power3.inOut`)
- [ ] `bounce` curves used sparingly (≤ 2 elements per page)

## Stagger (Principle 2)

- [ ] Lists / grids stagger their reveal — never simultaneous
- [ ] Total stagger time ≤ 800ms regardless of item count
- [ ] Per-item delay is 40–120ms depending on count
- [ ] Stagger applies to *peer* elements only, not nested children

## Fade (Principle 3)

- [ ] No `opacity 0 → 1` without an accompanying transform
- [ ] Fade durations: 200ms (UI) to 800ms (hero), nothing in between
- [ ] Reveals fire once per element (`once: true` on ScrollTrigger)

## Morph (Principle 4)

- [ ] Morphs connect *conceptually identical* states only
- [ ] Duration 300–600ms — not snappier, not slower
- [ ] Easing is `power3.inOut`, not ease-out

## Masking (Principle 5)

- [ ] Masks use `clip-path`, not `overflow: hidden` + size animation
- [ ] Element either masks OR fades, not both
- [ ] `will-change: clip-path` set on the masked element

## Dimension (Principle 6)

- [ ] Max tilt ±8°
- [ ] `transformPerspective` set (1000–1500)
- [ ] Card resets to flat on `mouseleave`
- [ ] Disabled on `prefers-reduced-motion`
- [ ] Disabled below 768px viewport

## Parallax (Principle 7)

- [ ] `ease: "none"` on parallax tweens (scrub provides the curve)
- [ ] `scrub: true` set
- [ ] Disabled below 992px viewport (or values halved)
- [ ] ≤ 4 parallax layers per section
- [ ] Smooth scroll (Lenis) layered in if parallax is on the page

## Zoom (Principle 8)

- [ ] Scroll-driven zooms use `pin: true` and `anticipatePin: 1`
- [ ] `scrub: 1` (or `3` for long sections) — not `true`
- [ ] Max scale jump ≤ 2.5x
- [ ] `will-change: transform` on the zoomed element

## Performance

- [ ] No layout-thrashing properties animated (`width`, `height`, `top`, `left`)
- [ ] All animation properties are `transform` / `opacity` / `filter` / `clip-path`
- [ ] `will-change` declared on animated elements
- [ ] Heavy `<img>` parallax has `loading="eager"` on first-fold layers only
- [ ] Lottie files lazy-loaded per viewport (not all 30 at once)

## Accessibility

- [ ] `prefers-reduced-motion: reduce` honored — animations either disabled
      or reduced to a near-instant fade
- [ ] Focus visible during transitions (no `outline: none`)
- [ ] Animations don't trap keyboard navigation
- [ ] Parallax doesn't push critical content out of the viewport

## Mobile sanity

- [ ] Tested on a real iOS device (not just Chrome DevTools)
- [ ] No "fade-in-only" reveals fire above the fold (user sees nothing on load)
- [ ] Hover-only effects have a touch alternative or are disabled on touch

## Final feel test

- [ ] Refresh the page 5 times and watch the hero. Does it feel
      *intentional* or *busy*?
- [ ] Show it to one person who hasn't seen it. Do they notice the
      motion, or do they notice the *content*?
- [ ] If the motion is what they notice first, you've gone too far.
