---
title: "The OG review — vision, what went wrong, and how we finish"
date: 2026-09-26
status: corrected 2026-09-26 — the live concept stands; this review lists bugs and skills only
withdrawn_storyboard: https://claude.ai/artifact/CXSsd4HTGzVZaZTuCiTpp4 (reverted the founder's concept; do not build from it)
---

# The OG review

*Read it before touching `site/`.*

---

## ⚠️ Correction, 2026-09-26

The first version of this review (and the storyboard linked in its front matter) was **wrong**.
It proposed replacing the live concept with a normal-flow scroll page, cut the logo apart again,
and restored copy the founder had deliberately removed. **All of that is withdrawn.** The
storyboard at that link is superseded and must not be built from.

## 1. The vision, as the founder actually set it

These are founder decisions recorded in commits 1d2a6ca, 821d81a and 81ad174. They are settled,
so don't re-litigate them.

- **The feeling is ふわふわ.** It is soft, floaty and weightless, with no hard edges.
- **The arrival is the whole site.** The logo is used **whole and uncut**, STUDIO included,
  sitting on the painted clouds. *"There is one mark."* Never dissect it.
- **Scrolling parts the cloud and the mascot once.** Behind them is the sky itself, with **all
  three dreams floating in it at the same time**: a place, not a slideshow. The Kits leads and
  is larger. Couple App reads as a presence, not a hole.
- **Names only in the sky.** Each description is the first thing on that field's own page, one
  click away.
- **The creed and the closing stay removed, at the founder's word.** Where "Happy to be reached
  out to." should live is still an open founder decision.
- **Click a dream to enter its field, then go deeper to reach the forest within.**
- **Back lands in the open sky** with all three dreams showing.

## 2. What is actually wrong with the live site (bugs, not concept)

The concept is right. These are execution bugs, measured on the built site:

1. **The no-JS, reduced-motion and after-Back layout is broken.** The logo lands on top of the
   Whimsy painting (`index.astro:230` with `Mark.astro:48`).
2. **`ClientRouter` strips `html.js` on navigation** (`Layout.astro:37`), which drops the page
   into that broken baseline and kills the mascot's paint script.
3. **The Googlebot expanded-viewport render is 21,600px with every dream invisible.** The frame
   height is uncapped (`index.astro:293`).
4. **Keyboard focus lands on an invisible link** (`index.astro:321`).
5. **On a phone the dreams are 56–98px wide** (sizes are in vw, `index.astro:333-335`), and
   there is a band of empty sky between the mark fading and the first dream.
6. **The mark's breathing animation is overridden** by `mark-away` (`index.astro:192-194`).
7. **Field-page height changes while you scroll** (`Field.astro:84-89`).
8. **Nothing protects the minifier fix** (`cssMinify: 'esbuild'`). CI never smoke-tests the
   built page, which is how a week-long outage went unnoticed.

## 3. How to finish it: polish the live concept, don't replace it

1. **Verification harness first.** Run Playwright against `astro build && astro preview`, never
   dev. Cover 390px and 1440px, reduced motion, no JS, 1024×8000, Tab focus, and Back from a
   field. Wire it into `deploy.yml`.
2. **Fix bugs 1–8**, keeping the landing frame pixel-identical.
3. **Polish the parted sky and the phone layout**, and show the founder before and after
   screenshots of the *live* frames before committing. Anything that changes the concept goes
   to the founder first.

### Rules of the house

- **Start from the live site, always.** Read the commit messages for founder decisions before
  proposing anything.
- **Verify the build, never dev.** Screenshots or it didn't happen.
- **No new architecture without a written reason and the founder's OK.**

## 4. Skills: what the OG loaded into this project

Researched online, downloaded, and read in full before installing. Every bundled script was
checked to be read-only, with no network calls and no telemetry.

| Skill | Source | Why it's here |
|---|---|---|
| `frontend-design` | Anthropic, official | Restraint: *one orchestrated moment*, spend boldness in one place, critique from screenshots. ⚠️ It lists "warm cream background" as an AI-slop tell. **Your cream is sampled from the logo, and the skill itself says the brief wins.** Keep the cream. |
| `webapp-testing` | Anthropic, official | Playwright against the *built* site. It's the direct cure for root cause #1. |
| `performance`, `core-web-vitals`, `web-quality-audit` | Addy Osmani (Chrome team), MIT | Measurement-first Lighthouse and Core Web Vitals, for the ≥95 bar. |
| `astro`, `astro-transitions`, `astro-images`, `astro-perf` | astro-skills (J. Parra Crespo), MIT | `astro-transitions` recommends native View Transitions over ClientRouter, which is exactly the fix. The scanner ran clean on this repo. |

**Kept:** `gsap-core`, `gsap-scrolltrigger`, `gsap-timeline`, `gsap-performance`,
`gsap-utils`, `scroll-experience` and `accessibility-auditor`.

**Deliberately not loaded:**
- `seo` and `best-practices`, because they belong to Stage B.
- Addy's `accessibility`, which overlaps `accessibility-auditor`.
- `theme-factory`, because it picks a theme and yours is already set.
- `web-artifacts-builder`, which is the wrong deliverable.

**Recommended to retire (your call, not done):**
- `gsap-react` and `gsap-frameworks`: there's no React, Vue or Svelte here.
- `gsap-plugins`: it leads with ScrollSmoother, which breaks your "smooth scroll must be
  additive" rule.
- `zajno-motion`: it pushes agency-slick motion and Lenis, which is the reference-site
  whiplash that cost you a day.

Fewer skills means less noise pulling the build off course.

---

## 5. Decisions only you can make

The storyboard proposes an answer for each; confirm or change them on the canvas.

| Question | Storyboard proposal |
|---|---|
| Visitor-facing labels | Production names only, plus "Explore The Kits", "See the forest within" and "Back to the sky". No "dream field 01". |
| Where Seonso and Grumpy Carrot appear | **Open.** Frame 2 (Drift) is the natural place. How they're drawn is yours to decide. |
| Does the mascot come with you? | It floats in the arrival, reappears at the floor, and sits small in the field's corner as the way home. |
| Whimsy and Couple App fields | Same pattern as The Kits. Couple App stays mist until it has a name. |

## 6. Art to-do

- The cut-out mascot used in the storyboard was keyed from the logo automatically. A little of
  the logo's tan ground shadow remains between the easel legs, where it is the same colour as
  the wood. It needs a five-minute hand cleanup in any paint app before it ships.
