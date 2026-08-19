---
title: "Stage A2 — the art pass BUILD_PLAN.md Phase 1 demanded"
date: 2026-08-19
status: ready to build — awaiting GO
audience: self-contained; extends BUILD_PLAN.md Stage A, does not replace it
---

# Stage A2 — Remediation: the still frame first, then depth

## Why this plan exists

The first Stage A execution completed BUILD_PLAN.md's checkboxes but violated its
design instructions. The audit:

| BUILD_PLAN.md instruction | What happened |
|---|---|
| "Design the static frame first… **If it is not beautiful motionless, motion will not save it**" | Skipped. Built layout + motion wiring with no designed frame |
| "Layer **art** as separate transparent PNG/SVG: far → mid → subject → near → foreground" | No art authored. CSS gradient ovals substituted for illustration |
| DESIGN_SYSTEM §6: soft outline, darkened-fill line, gentle shading, match the logo | Cloud layers have none of these properties |
| "Still a creative call — decide during Stage A" (mascot accompaniment, field placement, visitor-facing labels) | Silently defaulted, never decided |
| Done-condition: Lighthouse ≥ 95 mid-range mobile | Never ran |
| Verification: Google's scroll-diff script | Never ran |

What survives from the first pass and is **not** redone: the Astro/GH Pages setup,
tokens, fonts, crawler guardrails (100svh cap, content-in-HTML, reveal backstops),
the forest data system (collection → generic Scene, fixtures), Lenis smooth scroll,
the scroll-timeline engine, deploy pipeline. This plan is the art and composition
pass on top of that working skeleton.

## Standing rules for every phase below

- All ten guardrails from BUILD_PLAN.md apply unchanged.
- **Copy rule (founder, 2026-08-19): founders' words, minimally edited. No new
  prose, no meta-narration.** This plan touches no copy.
- Every asset follows DESIGN_SYSTEM §6: palette from §1 only, outline = darkened
  fill (never black), soft variable line, flat-with-gentle-shading. SVG for flat
  vector, optimised; stable URLs in `public/`.
- Five layers maximum per composition (§6 layering budget).
- Reduced motion = the primary design. Every phase's output must be complete
  motionless — that is now the whole point.

---

## Phase A2.0 — The still frame

**Design before code. Nothing else starts until this frame is right.**

- [ ] **Draft the Dreamland art spec as a design-system amendment.** The system
      (§1, §6) requires additions to be deliberate changes to the document — so
      the vocabulary gets specified before anything is drawn: cloud anatomy
      (lobe construction, outline weight, shade/highlight tone per size class),
      sky pigment scale by depth, mascot cut-out spec, feather-mask values,
      occlusion rules. Proposed as a new section of `brand/DESIGN_SYSTEM.md`;
      every asset in A2.0–A2.3 consumes only what this spec defines.
- [ ] **Preserve the reference image's actual art — it is the design language.**
      The first pass replaced the arc lettering with plain Baloo 2 and cropped
      the mascot into a cream box: the one reference the system is derived from
      got butchered. Fix by extraction, not imitation: key out the near-uniform
      cream ground (PIL), clean the edges, and export as separate transparent
      assets at full resolution —
      1. the **arc wordmark lettering** (its white outline makes it sit on any
         sky) — used as the arrival's title art, with real `<h1>` text kept
         underneath for crawlers and screen readers;
      2. the **mascot at its easel** — the studio's mark, floating boxless.
      Nothing about the mark gets redrawn in type or approximated.
- [ ] **Build the cloud vocabulary.** Lobed, puffy SVG cloud shapes — the logo's
      own silhouette language, not gradient smears. Per §6: mint/mint-soft fills,
      `--sage`-dark outline, one highlight + one shade tone per cloud. Three sizes
      (small wisp / mid puff / large bank), 2–3 variants each, one shared SVG
      sprite. These are the *only* cloud assets the site uses, everywhere.
- [ ] **Compose the arrival frame as a still.** Sky gradient with real pigment
      (not three near-whites), cloud banks placed deliberately, the cut-out mascot
      floating, title at display scale (clamp ~5rem–8vw), scroll hint. Compose at
      mobile, laptop, and wide.
- [ ] **Founder eyeballs the motionless frame and approves it.** This is the
      "is it clouds?" creative call from BUILD_PLAN.md being decided for real,
      on a real image. Iterate until approved — cheap now, impossible later.

**Done when:** the founder says the still frame is right. Not before.

---

## Phase A2.1 — Depth with occlusion

Motion only after the frame earns it.

- [ ] **Restack for occlusion.** Far + mid cloud layers behind content; one near
      layer *in front of* content (`pointer-events: none`), so silhouettes cross
      titles and islands while scrolling. Depth = things passing in front of
      things, not wallpaper sliding behind cards.
- [ ] Parallax speed ratios per the skill tables (far 0.2× / mid 0.5× / near
      0.9×+), distances sized so lobed silhouettes visibly cross — featureless
      motion was invisible; shaped motion reads.
- [ ] **Journey height and beats.** ~5–6 screens: arrival → drifting intro line →
      field 01 → field 02 → field 03 → floor. Each beat gets its own composition
      weight — not five identical centered panels.
- [ ] **Mascot accompaniment — decide it.** Proposed: the mascot drifts down with
      the visitor from arrival toward the first field (scroll-linked, transform
      only), then waves off; holds at rest under reduced motion. Confirm or reject
      at review.
- [ ] Sky warms as you sink (already wired) — retune against the new pigment.

**Done when:** scrolling shows silhouettes occluding content; the static fallback
frame is still complete; mobile offsets halved.

---

## Phase A2.2 — The fields as dreams

- [ ] **Dissolve the field art into the sky.** Feathered `mask-image` gradients
      so each reference image fades out at its edges — no rectangles, no hard
      blob frames anywhere on the hub.
- [ ] **Seat each island** with overlapping cloud lobes from the A2.0 vocabulary,
      near-layer lobes crossing the art's lower edge.
- [ ] Couple App stays an unformed dream: same cloud vocabulary, fewer lobes,
      less resolved — mist built from the real shapes, not generic blobs.
- [ ] Hover: island lifts + mint glow (kept); near lobes shift a few px
      (dimension principle, subtle, `transform` only).

**Done when:** no rectangular or hard-framed art exists on the hub, and each
island reads as *in* the sky rather than pasted on it.

---

## Phase A2.3 — Field pages and the forest re-skinned

- [ ] Field heroes adopt the same cloud vocabulary: feathered art, wisps that
      occlude the header edge, accent tint kept subordinate to studio tokens.
- [ ] **The forest stops being white SaaS cards.** Scenes sit on soft ground
      washes inside the grove; the sapling/grove distinction becomes visual
      growth — a sapling is one small sprout composition, a grove is a clustered,
      denser, taller one. BUILD_PLAN.md Phase 3's own words: "the difference
      should be **felt**, not just labelled."
- [ ] The `Scene` component stays fully data-driven — a new month still never
      touches code. Re-skin only.

**Done when:** a visitor scrolling a field page never leaves the world; the grove
visibly outgrows the saplings.

---

## Phase A2.4 — The verification the first pass skipped

- [ ] Lighthouse ≥ 95, mid-range mobile profile, all four pages
- [ ] Google's scroll-diff script (`lazyimages_without_scroll_events.js`,
      GoogleChromeLabs/puppeteer-examples)
- [ ] Re-run: `curl -A "GPTBot"` all pages · expanded-viewport sim (1024 × page
      height) · reduced-motion pass · keyboard/focus pass
- [ ] Bundle check: every JS/CSS chunk < 2 MB uncompressed (CI already enforces)
- [ ] Deploy, founder review on the live URL

**Done when:** every box above passes on the live site, and the founder signs off
on the feel — which is the actual Stage A exit condition BUILD_PLAN.md set.

---

## Decisions this plan surfaces instead of defaulting

| Decision | Status | Where it lands |
|---|---|---|
| Is it clouds? | **Decided by the A2.0 still-frame review** — on an image, not an assumption | A2.0 |
| Does the mascot accompany you? | Proposal in A2.1, founder confirms | A2.1 |
| What visitors see labelled ("dream field 01", "the forest within" are internal vocabulary currently shipped as-is) | **Open — founder call.** Costs one string edit whenever decided | any time |
| Where the personas appear / hand over | Untouched by this plan; still open from BUILD_PLAN.md | Stage A close |

## Not in this plan

Everything BUILD_PLAN.md defers: Stage B entirely (Cloudflare, SEO markup,
analytics, legal pages), the real Forest pipeline, any Whimsy wiring.
