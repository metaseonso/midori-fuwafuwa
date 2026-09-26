# The Passage: how the cloud parts

*From the OG. Read this before you touch `index.astro` again.*

You built this backwards. You opened the code, saw two paintings in `productions/*/reference/`,
and arranged the sky around them. Those paintings are temporary. They'll be replaced by art whose
composition nobody knows yet. The things that last are the logo, the cloud plates in
`public/images/dream/`, the palette and the founder's words: *"Scroll through the dream world,
explore a field, see the forest within."* and *"Scroll is for wandering. Click is for choosing."*

So we start from the visitor.

---

## 1. The visitor's journey, beat by beat

Percentages are of the **journey**: the pinned travel from the arrival to the settled sky. They
are not percentages of the page, because the page ends when the journey ends.

| Beat | Journey % | What they see | Its emotional job |
|---|---|---|---|
| **0. Arrival** | 0 (still) | The whole logo sitting on painted clouds. The mascot breathes and the clouds drift. On a laptop the clouds frame all four sides. On a phone the logo sits a little above centre, with cloud above and below. | *"Oh, it's soft here."* Recognition and welcome. The eye goes to the mascot's face. |
| **1. Handshake** | 0–5 | The first wheel notch or thumb-drag moves the near clouds about **80px outward** and makes the mascot about **12% larger**. The chevron is gone by 4%. | Proof that scrolling *moves me forward*. If the first input only fades something, the visitor learns nothing. |
| **2. Approach** | 5–25 | The near clouds slide toward their own edges. The logo grows toward you and the far banks barely move. | Anticipation: *we're going in.* The eye stays on the mascot, which is getting closer. |
| **3. Crossing** | 25–55 | Wisps (the `motes` plate) stream outward from the centre. The logo passes the lens and dissolves into its own cream. The cream veil peaks at about 45%, and the near clouds leave the frame by then. | The held breath: *I went through the cloud.* Most visual change per pixel of scroll happens here. |
| **4. Emergence** | 45–85 | This overlaps the crossing on purpose. The dreams are already behind the veil, small and hazy, and they come toward you. The Kits clears first because it is nearest. The far banks settle in to hug the edges. | Wonder. The eye goes to The Kits, which is the largest, the clearest and the nearest. |
| **5. Settle** | 85–100 | The camera decelerates to nothing, and this whole stretch moves things by under 12px. The names rise into full ink. The page ends. | Rest, then choice. |

**What tells them to keep scrolling:** the handshake, not the chevron. The world answers the very
first input with movement *toward* something.

**What tells them "you can click this":** the dreams stop moving, and then the names arrive last
and sharp. Anything that holds still in a world that just moved reads as an object. On a laptop,
hovering lifts the dream and changes the cursor. On a phone, a press gives a small squash on
`:active`. No copy is needed, and the founder removed the copy anyway.

**How they know it's over:** four signals arrive together. Motion stops answering the scroll. The
scrollbar hits the bottom, and on iOS the rubber-band shows more of the same paper colour. The
frame is closed on all four sides. Nothing waits below. Any scroll after the settle is a broken
promise.

**Click:** the painting lifts, and then it becomes the field page's hero through a shared-element
View Transition while the sky sinks away (`--dur-scene`, 600ms).

**Back:** the visitor lands in the open sky with all three dreams showing, which is the founder's
own requirement. Because every frame is a pure function of scroll position, the bfcache and scroll
restoration give this to you for free. The painting morphs back into its slot. This is the best
argument for scroll-driven animation over time-triggered animation.

---

## 2. The effect, named

In film this is a **dolly-in through a multiplane set**. Disney built the multiplane camera in
1937 to do exactly this: painted glass plates at different distances, with the camera travelling
toward them. Flying through a cloud bank is its most famous use. Five cues make it read as
**passage** and not as a transition:

1. **Radial expansion from a vanishing point.** Every plate moves *away from the centre* toward
   its nearest edge. Nothing converges.
2. **Differential scale, which is hyperbolic.** Projected size is `s = d₀ / (d₀ − c)`, where
   `d₀` is the plate's starting distance and `c` is how far the camera has travelled. Near plates
   explode, while far plates barely change. That ratio *is* the depth.
3. **Occlusion order that never lies.** Nearer is always in front, all the way through.
4. **Atmospheric perspective.** Distance is hazier and closer to the sky colour. Objects clear as
   you approach.
5. **The crossing.** There is a moment when the nearest plate fills the frame, a soft whiteout,
   and then you emerge with things **still approaching**. This last point separates a passage from
   a crossfade. In a crossfade, A dims and B brightens in place. In a passage, B was always there,
   and you move toward it.

### Why the live site reads as a fade

These numbers come from the source and from the frames `d00–d12` and `m00–m12`:

- **The logo recedes while the clouds approach.** `mark-away` goes to `scale(0.955)` and
  `translateY(-84px)`, which is *away* from the camera, and it reaches `opacity: 0` by 8% of the
  scroll. Meanwhile the clouds scale *up*. The two depth cues contradict each other and cancel out,
  and what's left is "it faded".
- **The clouds hardly move.** `partScale` is 1.10–1.16 spread across 52% of the scroll, which is
  about 0.3% of size per percent of scroll. That's below perception at normal scroll speed.
- **The front islands move the wrong way.** They rise by `-13vh` and `-15vh` toward the middle of
  the frame (see `m03`: the clouds climb into the centre). That is convergence, which reads as the
  cloud closing.
- **Every plane shares one range (0–52%) and a linear timing function.** With no separation in
  time, the stack moves like one card.
- **There is dead air in the middle.** The mark is gone at 8% and the first dream starts at 30%,
  which leaves roughly 37vh of empty sky (`d02–d03`). At that point, the thing you passed through
  is gone and the thing you're arriving at isn't there yet.
- **The dreams materialise in place.** They go from opacity 0 to 1 and from `scale(.9)` to `1`
  at fixed positions, with no haze, no occlusion and no approach. They are stickers on the sky, not
  objects in it.
- **The timing is glued to `scroll(root)`.** Everything is a percentage of the whole document, so
  the last dream settles at 74% and the rest is dead scroll (`d07–d12` are identical).

---

## 3. How a professional builds it

### 3.1 The layer stack

The camera travels `c: 0 → 1`, and `d₀` is each plane's starting distance. The table uses only
permanent assets, plus the three slots.

| Plane | `d₀` | Role | End state |
|---|---|---|---|
| `island-base`, `island-misty` | 1.2 | Near foreground. It grazes the mascot. | Exits left and right edges by about 45%. |
| Mark (whole logo) and its cream glow | 1.4 | The cloud you pass *through*. | Dissolves into cream from 30% to 55%. |
| `motes` (×2, mirrored) | 1.55 | Wisps inside the cloud. They carry the crossing. | Hidden until 20%, then stream out and are gone by 80%. |
| `sky-mid` (band-trimmed) | 2.2 | Lower bank. It occludes the lower edge of the dreams. | Hugs the bottom edge. |
| Dream slots: Kits, Whimsy, Couple App | 2.5, 2.9, 3.1 | The sky's contents. | Settle at 1.0. |
| `sky-far` (band-trimmed) | 3.6 | Upper bank, behind the dreams. | Hugs the top edge. |
| Sky gradient | ∞ | The stage background. | Never moves. |

Leave out `sky-near` and `sky-front`. They are hard rectangles on all four edges, as the alpha
measurements in `index.astro` already show.

### 3.2 The camera model

Use one eased camera and derive every plane from it:

```
c(p) = 1 − (1 − p)²          ease-out dolly: it starts at once and decelerates into the settle
s(p) = d₀ / (d₀ − c(p))      arrival plates: s(0) = 1, so the landing frame is pixel-identical
s(p) = [d₀/(d₀−c)] / [d₀/(d₀−1)]   dreams: normalised so s(1) = 1
```

| p | 0 | .10 | .25 | .40 | .50 | .60 | .75 | .85 | 1 |
|---|---|---|---|---|---|---|---|---|---|
| islands (1.2) | 1.00 | 1.19 | 1.57 | 2.14 | 2.67 → exited | | | | |
| mark (1.4) | 1.00 | 1.16 | 1.45 | 1.84 | 2.15 | 2.50 → gone | | | |
| sky-mid (2.2) | 1.00 | 1.09 | 1.25 | 1.41 | 1.52 | 1.62 | 1.74 | 1.80 | 1.83 |
| Kits (2.5) | .60 | .65 | .73 | .81 | .86 | .90 | .96 | .99 | 1.00 |
| Whimsy (2.9) | .66 | .70 | .77 | .84 | .88 | .92 | .97 | .99 | 1.00 |
| sky-far (3.6) | 1.00 | 1.06 | 1.14 | 1.22 | 1.26 | 1.30 | 1.35 | 1.37 | 1.38 |

The good part is that an ease-out camera combined with hyperbolic projection gives near plates an
*accelerating* rush and far plates a *decelerating* settle, from one curve. The last 15% moves
The Kits by 1% of its size, which is the settle you want. **Tune `d₀`, never individual
keyframes.** The founder's "modest opening" is a matter of the far planes' `d₀` values.

**Ship it baked.** Generate the keyframes in Astro frontmatter at build time, using about 11 stops
per depth. You could animate a registered `@property --cam` and `calc()` each scale from it, and
that's great for prototyping with a slider. However, custom-property animations run on the main
thread, and baked `transform` keyframes run on the compositor.

### 3.3 Clouds exit; they don't fade

Put each plate in a **rig**: a full-stage wrapper whose `transform-origin` *is* the vanishing
point. Scaling the rig then pushes the plate radially toward its own edge, which gives you the
founder's "each cloud aimed at one edge" for free.

```css
.rig { position: absolute; inset: 0; transform-origin: 50% 46%; /* the mascot's belly */
       animation: var(--kf) linear both;
       animation-timeline: --journey; animation-range: contain 0% contain 100%; }
/* baked keyframes end with the retire: */
@keyframes d120 { /* ...scale stops... */ 45% { transform: scale(2.4); visibility: visible; }
                  46%, 100% { transform: scale(2.4); visibility: hidden; } }
```

Keep one motion channel per element: the rig carries the scroll camera, the plate carries the
pointer `translate`, and the `<img>` carries the ambient drift. Two `animation` declarations on
one element overwrite each other, which is exactly why the mark's breathing is dead today (bug 6).

Only use opacity to retire a plate that has *already left the frame*, or on the crossing veil. Cap
a layer's maximum keyframe scale at about 2.5 and end its keyframes once it is off-frame, because
the compositor may rasterise for the largest scale it sees. The plates are 1200px wide, so a near
plate going soft as it rushes past is correct optics. A far plate going soft is a bug.

### 3.4 The mascot plane: through, not away

The logo is RGB on the cream `#F4EDD6`, with a feathered mask. So when it scales past about 2×,
its own cream fills the frame, and *that is the whiteout*. You fly into the mascot, which is a
cloud, and out the other side. It stays whole and uncut the entire time.

The art fades first (opacity 1 until p .22, 0.35 by .40, 0 by .52), before the letterforms loom.
The glow holds until .55 and carries the veil. Aim for a peak of about 75% cream, not 100%, so
some sky shape survives and it never reads as a blank page.

### 3.5 The dreams approach and settle

Each dream rig scales about the same vanishing point from 0.60–0.68 to 1. Off-axis objects
therefore drift *outward* from the centre as they approach: The Kits starts at about 38% across
and settles at 30%. The dreams come apart from the middle of the parting. Their haze veil reaches
zero at rest, because DESIGN_SYSTEM §6 doesn't let you dim painted art. At rest, depth is carried
by size, position and occlusion.

### 3.6 Easing per layer

The baked curve is the easing, so run each stop linearly between them. Names fade and rise 8px
over p .72–.92. The mascot keeps `--ease-bounce` for its "notice" and nothing else uses it.
Ambient drift stays linear and alternating, as it is now.

### 3.7 Scroll budget: zero dead scroll

```css
.journey { --travel: min(140vh, 1260px);
           height: calc(min(100svh, 900px) + var(--travel));   /* capped: ≤ 2160px anywhere */
           view-timeline: --journey block; }
@media (max-width: 600px) { .journey { --travel: min(115vh, 970px); } }
```

That's 1.4 viewports on a laptop and 1.15 on a phone. At a relaxed trackpad pace of about 70vh/s,
the crossing (30% of the travel) lasts about 0.6s, which matches `--dur-scene`. Bind to a **named
view timeline on the journey**, never to `scroll(root)`, so that a Stage B footer can never retime
the sequence. The document ends at the journey's end. If Stage B needs a legal line, it goes
*inside* the settled frame's bottom edge.

### 3.8 Pinning that stays crawler-safe

The baseline is **two capped panels in normal flow**: the arrival, then the sky with the three
dreams in their constellation. This is the still composition, it is complete, and nothing in it
overlaps. The cinematic stacks the sky over the arrival only when it's safe:

```css
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) and (min-height: 480px) and (max-height: 1500px) {
    html.js .stage { position: sticky; top: 0; height: min(100lvh, 900px); overflow: clip; }
    html.js .sky   { position: absolute; inset: 0; }
  }
}
```

The `max-height: 1500px` gate matters most. Googlebot's expanded 1024×8000 viewport fails it, so
it gets the baseline with every dream visible. Don't rely on an "inactive" timeline showing base
styles. This repo's own `reveal-fallback.js` records timelines sticking at `opacity: 0` on tall
viewports.

Some rules that follow from this:

- Keep every word and `<img src>` in the HTML.
- Remove `ClientRouter` so `html.js` survives navigation.
- Use `100lvh` for the stage so it never resizes mid-scrub, and keep dreams and labels inside the
  top `100svh`.
- `overflow: clip` is fine here, because the clip edge *is* the viewport edge.

### 3.9 CSS or JS

Native scroll-driven CSS handles all of it. Firefox currently has no scroll-driven animations, so
it gets the still composition, which is the finished design. Add GSAP only with a written reason,
for example if the founder decides Firefox must have the passage and the traffic numbers justify
it. Never add Lenis.

The only JavaScript: the mark's existing pointer script, and a focus handler (§4).

### 3.10 Performance budget

The jank was measured once already, and it came from **raw layer area**. So:

- Have no more than 8 layers animating at once, by retiring plates as they exit.
- Keep peak drawn area under about 3.5× the viewport on a laptop and 3× on a phone, measured by
  summing layer visible-rects through the CDP `LayerTree` domain.
- Band-trim the far plates, as they are now.
- Don't use permanent `will-change`, because scroll timelines promote the layers themselves.
- Check in the Layers panel that each rig's layer is plate-sized. If a rig inflates to the full
  stage, bake `(s−1)·offset` into `translate` instead.

The target is **under 1% of frames over 20ms** on a laptop and **under 5% at a 4× CPU throttle**.

### 3.11 Mobile is a different composition

A portrait frame is not a small landscape one.

- Put the vanishing point at about 44% height.
- The side islands exit laterally almost immediately, so the top and bottom banks carry the
  framing.
- The constellation stacks diagonally: Kits at (50%, 43%) at `clamp(200px, 60vw, 260px)`, Whimsy
  at (72%, 13%) at `clamp(128px, 36vw, 170px)`, and Couple App at (30%, 75%) at
  `clamp(120px, 34vw, 160px)`.
- Tap targets are the whole painting plus its name.
- Touch has no hover, so `:active` gives the feedback.

### 3.12 Reduced motion and no-JS

Both get the two-panel baseline: the arrival exactly as it is, then the open sky. Nothing moves,
nothing is hidden and nothing overlaps. It is still the design.

---

## 4. The dream slots

Design the **slot**, not the painting. Each slot takes `{src, alt, focal}`, where `focal` is an
`object-position` so that future art can name its focal point. Couple App's bloom goes in the same
slot with the same behaviour.

- **Frame:** a square slot, `object-fit: cover`, and a centre-weighted radial mask that feathers
  from 62% to 100%. That is aspect-agnostic, and it never shows a rectangle.
- **Depth haze:** a `::after` in `--paper` whose opacity runs 0.6 → 0 over p .45–.85. It is
  opacity only, and it's zero at rest.
- **Near-cloud occlusion:** `sky-mid` crosses only the lower-outer 10–15% arc of each slot,
  inside the zone the mask already feathers. It never reaches the centre, because you can't know
  where a future painting's subject sits.
- **Desktop sizes:** The Kits `clamp(320px, 27vw, 440px)` at (30%, 50%), Whimsy
  `clamp(220px, 18vw, 300px)` at (71%, 32%), Couple App `clamp(180px, 14vw, 240px)` at
  (57%, 72%). Check these at 1440×900, 1024×768 and a 2:1 aspect.
- **Labels:** labels don't scale with the camera, so they are crisp at rest. Use `--ink` (10.86:1)
  with a static halo, `text-shadow: 0 0 .5em var(--paper), 0 0 1.2em var(--paper)`, so the names
  stay readable over pink cloud. Sizes are 2rem, 1.5rem and 1.3rem.
- **Affordance:** on hover or focus, the dream lifts with `translate: 0 -6px` and `scale: 1.03`,
  and a pre-painted glow behind it goes from opacity 0 to .8. It takes `--dur-ui` with
  `--ease-out-soft`. Use no animated `box-shadow`. For focus, add
  `outline: 3px solid var(--mint-deep); outline-offset: 6px; border-radius: 50%`.
- **Focus is a scroll too.** When a dream receives focus before the sky is open, move to the end
  of the journey:

  ```js
  el.addEventListener('focus', () => { const j = document.querySelector('.journey');
    const end = j.offsetTop + j.offsetHeight - innerHeight;
    if (scrollY < end - 2) scrollTo({ top: end, behavior: reduce ? 'auto' : 'smooth' }); });
  ```

- **Click → field:** drop `ClientRouter` and use `@view-transition { navigation: auto; }`. Give
  the dream's art `view-transition-name: kits-art` and give the field's `.fhero__img` the same
  name, so the painting becomes the hero. Keep the existing reduced-motion block that zeroes
  View Transition animations.

---

## 5. How to verify it like a pro

Always use `astro build && astro preview`, never dev. The minifier bug only exists in the build.

1. **Filmstrip at fixed journey percentages.** Capture 0, 3, 10, 25, 35, 45, 55, 65, 75, 85,
   95 and 100 at 1440×900, 1024×768, 390×844 and 360×740. Wait two rAFs after each scroll.
   Pixel-diff neighbouring frames: any pair before 100% that falls below the threshold is dead
   scroll. Assert that the maximum scroll equals the journey's end within ±2px.
2. **Video.** Record a smooth wheel scroll with Playwright's `recordVideo`, then watch it. The
   filmstrip catches bugs, and the video catches feeling.
3. **Device class.** Scrub with a 4× CPU throttle. Frame timing must stay within budget, and the
   LayerTree area must stay under the cap.
4. **Boxes at 100%.** Check that dream widths are at or above the minimums, that no two dreams or
   labels overlap, that every label is inside `100svh`, and that nothing overlaps the logo in any
   state.
5. **Reduced motion and no-JS.** Take a full-page shot of each: two panels, everything visible, no
   overlap, and nothing moving across two captures taken 1s apart.
6. **1024×8000.** The page should be under about 2200px tall, and every dream should compute to
   `opacity: 1`.
7. **Keyboard.** Tab to each dream. The page scrolls to the open sky, and the focus ring is
   visible in the screenshot.
8. **Back.** Click The Kits at 100%, go back, and assert that `scrollY` equals the end and all
   three dreams are visible.
9. **Raw HTML.** `curl -A GPTBot` must show all three names, all alts and the `<h1>`.

---

## 6. The three most common ways juniors ruin this effect

**1. They let opacity tell the story.** The screenshot tell: a mid-sequence frame that looks like a
double exposure or like empty sky (`d02`, `m03`). Put two frames 10% apart side by side. If the
cloud silhouettes are in the same place and only their transparency has changed, it's a crossfade.
In a passage, the middle frames show things *bigger and nearer the edges*, never "less there".

**2. They move everything at the same rate, or in contradicting directions.** The tell: overlay
the first and middle frames and draw each plate's displacement. If the arrows are parallel and of
equal length, you have one flat card. If they point *inward*, or the logo shrinks while the clouds
grow, you have convergence. A real push has arrows pointing radially outward, and the near arrows
are at least twice as long as the far ones.

**3. They glue the timing to the page and the sizes to vw.** The tell: a filmstrip whose last
third is identical frames (`d07–d12`), 56px thumbnails on a phone (`m08`), and a 21,600px grey
tower in the 1024×8000 capture. The fix is the same every time: a named view timeline on a capped
journey, `clamp()` sizes with pixel floors, and a page that ends when the sky settles.

Start from the visitor. The code only has to keep up with them.
