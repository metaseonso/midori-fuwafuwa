---
title: "The OG review — vision, what went wrong, and how we finish"
date: 2026-09-26
status: awaiting founder approval of the storyboard
storyboard: https://claude.ai/artifact/CXSsd4HTGzVZaZTuCiTpp4
supersedes: the sequencing of BUILD_PLAN_A2.md (its guardrails and done-conditions still stand)
---

# The OG review

*Written from the seat of an old, experienced full-stack web developer who has watched many
beautiful ideas die in the build. Read it before touching `site/`.*

---

## 1. The vision, excavated

Nothing here is new. It is all yours, from `ETHOS.md`, `PROJECT.md`, the decision log and
the craft notes. It just got buried under 26 commits.

**The feeling is ふわふわ.** *"I like the fuwa fuwa feel more than the studio feel."* That means
soft, floaty and weightless: no walls, no floor, no hard edges, and depth from haze and layers
rather than lines. The mascot is a small mint cloud, and the site should feel like being
*inside* it.

**The movement is one sentence:**

> **"Scroll through the dream world, explore a field, see the forest within."**

| | Verb | What it is |
|---|---|---|
| The dream world | **Scroll** | Drifting down through the clouds. No decisions required. |
| A field | **Click** | One production's own world. A chosen threshold. |
| The forest within | **Go deeper** | That production's living history, a sapling per month and a grove per season. |

**The words are yours, and they are few.** *"A production studio based out of a Dreamland,
shared by Seonso and Grumpy Carrot."* *"She owns the muse. He owns the genius, as the Greeks
say."* *"We make it for ourselves too."* *"Happy to be reached out to."* Whimsy's voice stays
in Whimsy's field.

**There is one style reference: the logo.** Cream, mint, blush, sage, wood, and nothing else.

**The rhythm is real.** Month → sapling, season → grove. It is the same clock as the business,
the farm and Whimsy.

**The site collects nothing.** No forms, no tracking, no accounts.

The four value principles are to be *immersive yet minimalist*, *cute, fluffy and chibi*,
*snappy to render*, and *simple to produce*. That is a completely achievable site. Nothing in
this vision is technically hard. It was lost in execution, not in ambition.

---

## 2. What actually went wrong (the forensics)

A full build-by-build audit was run on every commit, including rebuilding historical versions
and screenshotting them. The short version:

1. **For a week the live home page was just the logo.** Astro's default CSS minifier silently
   rewrote every `animation-timeline` into an invalid shorthand, so the browser dropped it and
   all three fields sat at `opacity: 0`. Every "verified" note in those commits was measured on
   the dev server, never on the build. The same bug had been there since the first Stage A
   commit, so **no scroll animation ever ran in production before Aug 28.** It is fixed now
   (`cssMinify: 'esbuild'`), but nothing protects it.
2. **Five whole architectures in one day, then a revert.** They were: speed-factor parallax,
   WebGL sky, scale-through clouds, a fixed perspective stage, and a pinned "parting" hero. The
   swings came from copying reference sites (hadaka.jp is a single-screen WebGL page and nothing
   like your scroll-drift model), backed by jank numbers from a GPU-less headless browser that
   were later retracted.
3. **Your words were deleted to fix layout problems.** The creed, the closing, and "Happy to be
   reached out to" were removed, and the field descriptions are hidden whenever JS runs.
4. **The plan's gates were skipped.** A2 said *"the founder approves the still frame — not
   before."* That never happened. The design system was never amended, Lighthouse was never
   run, and the scroll-diff check was never run.
5. **The current build has real bugs that no commit mentions:**
   - With reduced motion, no JS, or after pressing Back, the logo lands *on top of* the Whimsy
     painting (`index.astro:230` with `Mark.astro:48`).
   - `ClientRouter` strips the `html.js` class on navigation, which breaks the crawler safety
     pattern and the mascot's paint script (`Layout.astro:37`).
   - The Googlebot simulation gives a 21,600px page with every field invisible, because the
     frame height is uncapped (`index.astro:293`). This breaks your own hard rule.
   - Keyboard Tab focuses an invisible link (`index.astro:321`), so focus is not visible.
   - On a phone the three dreams are 56–98px thumbnails, and there is a band of empty sky.
   - Inside a field the sky disappears into a flat mint page, and the forest reads as a
     changelog, not a forest.

**None of this is your vision failing. It is process failing.** That is good news, because
process is fixable.

What is genuinely good and stays: the painted cloud plates, the arrival still frame, Astro as a
static site, the tokens and fonts, the content-collection Forest with fixture recaps, and the
tiny payload (the whole site is 2.6 MB and weight was never the problem).

---

## 3. The OG's verdict

### Don't burn it down again. Finish it.

Every rebuild so far threw away something that worked. The foundation (Astro, the art, the
tokens, the Forest data) is right. What's wrong is the hub's scroll architecture and the
missing verification.

### The architecture, in plain terms

- **The hub is a normal page that scrolls normally.** It has five real sections in normal
  document flow: Arrival → Drift → The Kits → Whimsy and Couple App → The floor. Each is capped
  at `max-height: 900px`. There is no pinned stage, no fixed frame, and no scroll-jacking. This
  alone removes the 21,600px Googlebot bug, the overlap bug and the invisible-focus bug, because
  they all come from the pinned-stage trick.
- **Parallax lives inside each section**, using native CSS `animation-timeline: view()` on the
  painted layers. That's three speeds (far 0.2×, mid 0.5×, near 0.9×), `transform` and
  `opacity` only, and guarded by `@supports`. Without support you get the still frame, which is
  designed to be finished on its own. Phone distances are halved.
- **Entering a field uses native cross-document View Transitions.** It is zero JavaScript, the
  island morphs into the field hero, and field pages stay real URLs. **Remove `ClientRouter`.**
  That is the one change that fixes the `html.js` bug, the dead mascot script and the broken
  Back button.
- **The sky follows you into the field.** A field page is a painted world, not a flat mint
  document.
- **The forest grows visibly.** A grove is a cloud-canopied tree over its month-saplings, and a
  sapling is a small sprout. It stays data-driven, so a new month is a JSON file, never code.
- **GSAP stays in the toolbox, not in the page.** Nothing in the storyboard needs it. Add it
  only if a specific beat proves CSS can't do it, and write down why. Drop the unused `lenis`
  dependency.
- **Images go through `astro:assets`** for responsive widths and intrinsic sizes, with the
  arrival art eager and everything else lazy.

### Order of work

1. **Storyboard approval (founder).** Frames 1–8 plus the phone frames on the canvas. Nothing is
   built until you say those frames are right. This is A2's gate, finally held.
2. **Verification harness first, before any design work.** Write a Playwright smoke test that
   runs against `astro build && astro preview`, never the dev server. It checks 390px and
   1440px, reduced motion, no JS, 1024×8000, Tab focus, and that every field link is visible.
   Wire it into `deploy.yml` so a broken build can never deploy again.
3. **Fix the real bugs.** Remove ClientRouter, cap every section, restore your deleted words,
   make focus visible, and fix the Back behaviour.
4. **Build the hub sections** to the storyboard, still frame first, then parallax.
5. **Build the field page and field entry** (the sky continues, plus the view transition).
6. **Build the forest re-skin** (the grove outgrows the saplings).
7. **Build the phone pass** at 390px. The same story in one column, with 44px targets.
8. **Hit the done bar:** Lighthouse ≥ 95 on mobile for all four pages, Google's scroll-diff
   script, `curl -A GPTBot` readable, and your sign-off on the live URL.

### Rules of the house (for every session from now on)

- **Verify the build, never dev.** Screenshots or it didn't happen.
- **No new architecture without a written reason and your OK.** No copying reference sites.
- **Never delete your words to fix a layout.** Fix the layout.
- **One orchestrated moment.** Spend the boldness on the drift through the clouds and keep
  everything else quiet.
- **Edge-touching art always overhangs the frame.** A painted cloud cut by the viewport is a
  hard edge.

---

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
