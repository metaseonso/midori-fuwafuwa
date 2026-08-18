---
title: "Midori Fuwafuwa Studio — Website Reference"
date: 2026-08-18
status: research complete → build phase
---

# Midori Fuwafuwa Studio — website reference

**Start here.** This file is the single reference for building the studio website — everything below is the load-bearing summary; the three case study files behind it hold the full research, sourcing, and reasoning for anything that needs a deeper look.

## The studio, in short

Midori Fuwafuwa Studio is a production studio run by two artist-dreamers, **Seonso** (fox sage — calm, spiral-motif, black-and-gold) and **Grumpy Carrot** (bunny girl — chaotic, coffee-and-chocolate-fueled, pink-and-black), based out of a shared **Dreamland**. The mascot is a small fluffy mint-green cloud creature that paints at a tiny easel. Full brand reference: `brand/`.

## Value principles

- Immersive and informative, yet minimalist.
- Cute, fluffy, chibi as the intended visual outcome.
- Snappy to render.
- Assets simple to produce, in one consistent design language.

Everything below is an attempt to hold all four at once, not trade one off against another.

## Terminology: Field & Forest

The site has two halves, and two matching terms for them:

- **Field** — one production's own open, explorable diorama space. Replaces an earlier "room" idea: a Field is walkable and pastoral, not boxed in — closer to *Field of Dreams* than to a gallery room. Each production in the pipeline gets its own Field, reached from a central Dreamland map/hub. Built as 2D/2.5D layered parallax, chibi-illustrated, efficient by construction.
- **Forest** — that production's living continuity layer. Grows at the edge of its Field: a sapling per monthly consolidation, a fuller grove per season, sourced automatically from real GitHub activity on that production's repo. This is the "behind the scenes" destination — process and history, kept separate from the Field itself so the front-of-house stays calm and minimal while the Forest quietly thickens underneath.

*(This Field/Forest split is a proposed mapping onto the two case studies below — Field ≈ Case Study 01's output, Forest ≈ Case Study 02's. Worth confirming or adjusting once building starts; nothing downstream depends on the names themselves.)*

## System 1 — Fields (efficient immersive showcase)

Full detail: [`case-study-01-immersive-efficiency.md`](./case-study-01-immersive-efficiency.md)

- **Rendering approach:** 2D/2.5D layered parallax as the default — not full 3D. The chibi/flat-illustration style is already the cheapest thing to render well; layered PNG/SVG art at different scroll speeds reads as rich without the WebGL cost.
- **Scroll mechanism:** native CSS scroll-driven animations (`animation-timeline: scroll()`/`view()`) as the primary layer — compositor-only, no JS scroll listener, no jank under load. Lenis + GSAP ScrollTrigger layered in only for choreography native CSS can't express (pinned sections, scrubbed sequences), with `transform`/`opacity`-only discipline throughout.
- **3D/WebGL:** reserved for a single deliberate accent per Field (e.g. a glow/particle shimmer echoing Seonso's key art) — lazy-mounted on scroll-into-view, `frameloop="demand"`, skipped entirely under `prefers-reduced-motion`.
- **Structure:** each production is its own Field, entered from a central hub — not a portfolio grid. Palette accent and mascot pose vary per Field.
- **Personality:** performed by the mascots through small interactions (a hover animation, a loading-state spiral), not explained via an About page.
- **Front-page restraint:** minimal chrome, mystique-forward — process/technical depth lives in the Forest, not the Field.
- **Reduced-motion is the baseline, not a fallback:** designed first, since a static, softly-lit Field with mascots in resting poses is already a beautiful outcome — and it's also the fastest possible page.

## System 2 — Forests (the living pipeline)

Full detail: [`case-study-02-living-pipeline.md`](./case-study-02-living-pipeline.md)

Five stages, each naming the leading real component:

1. **Ingestion** — GitHub Actions `on: schedule` (monthly cron + seasonal/quarterly cron) pulls the period's commits/PRs/issues via GraphQL, and enumerates changed binary/art assets via the REST commits `files[]` array. *Watch item: scheduled workflows auto-disable after 60 days of repo inactivity — plan an external trigger or heartbeat.*
2. **Narrative synthesis + asset selection** — a Claude API call with structured/JSON-schema output turns the period's activity into an ordered scene script, referencing real committed asset filenames/SHAs. **This is the one genuinely custom step in the whole system** — no off-the-shelf tool does narrative-arc construction or story-relevant (vs. technical-quality) asset curation. Recommended pattern: tag new assets for mood/subject as they arrive, so the periodic synthesis call chooses from an already-curated pool.
3. **Storage** — a JSON manifest per production per period, committed back via `git-auto-commit-action`. Real art never moves; the manifest just references it.
4. **Rendering** — a static site generator with a content layer built for this (Astro Content Collections, or Eleventy's data cascade), reading the manifest through one generic, data-driven Scene component. This is the mechanism that means a new month's story never touches code, only data.
5. **Publish** — the manifest commit triggers a normal host rebuild (Cloudflare Pages/Vercel/Netlify). Consider routing through a PR rather than straight to `main` at first, as a cheap human-glance gate on AI-authored narrative before it's public.

## Tooling — Claude Skills priority order

Full detail, including overlaps/disqualifications and reasoning: [`case-study-03-tooling-and-protection.md`](./case-study-03-tooling-and-protection.md)

1. `claude-api` (official, bundled) — structured-output mechanic the Forest pipeline needs directly.
2. `skill-creator` (official) — build the two things this project actually needs custom: a narrative-arc-from-commits skill, and a Midori Fuwafuwa brand-consistency skill.
3. `webapp-testing` (official) — verify scroll/parallax/reduced-motion behavior on the local dev server.
4. `frontend-design` (official) — keeps output on-brand and away from generic "AI-slop" defaults.
5. `orchestrating-gsap-lenis` (community) — fixes the specific GSAP+Lenis conflict this stack will hit.
6. `gsap-scrolltrigger` + `threejs-webgl` (community, freshtechbro) — solid reference for the JS/WebGL layers; doesn't cover native CSS scroll-timeline or reduced-motion, so supplement rather than rely on solely.
7. `accessibility-auditor` (community) — serves the reduced-motion-first, minimalist-yet-informative principles directly.
8. `publishing-astro-websites-agentic-skill` (community, low-maturity) — useful reference for the content-layer setup; verify against current docs.

**Skip:** `web-artifacts-builder` (wrong deliverable shape — single-file artifact bundler, not a real multi-page site), `locomotive-scroll` (superseded by the Lenis decision already made), `theme-factory` (assumes picking a theme; this project enforces its own).

## Protection — practical order of operations

Full detail (informational, not legal advice): [`case-study-03-tooling-and-protection.md`](./case-study-03-tooling-and-protection.md)

1. A short founders'/IP agreement between the two collaborators, early — closes the default joint-authorship risk that either person can unilaterally license shared work.
2. Track which brand art has a clear human-authored backbone (worth formally registering, AI-assisted portions disclaimed) versus pure AI output (not independently protectable) — relevant given some brand art is AI-assisted.
3. Real Terms of Use / Privacy Policy once the Forest pipeline or any analytics goes live — a GitHub-API-backed site plus any tracking is enough to fall under current state privacy law.
4. Check font and third-party asset licenses before shipping, especially anything that might end up on merch later.
5. Trademark registration and formal business-entity formation are reasonable next steps once the studio is operating and the name is stable — not launch blockers, but worth planning for.

## File index

- [`synthesis-cross-findings.md`](./synthesis-cross-findings.md) — what the three case studies say *together*: shared shape, cross-connections, the open audience question, recommended build order.
- [`case-study-01-immersive-efficiency.md`](./case-study-01-immersive-efficiency.md) — efficient motion techniques, studio showcase patterns, the Field concept.
- [`case-study-02-living-pipeline.md`](./case-study-02-living-pipeline.md) — GitHub-driven auto-narrative research, honest novelty assessment, the Forest architecture.
- [`case-study-03-tooling-and-protection.md`](./case-study-03-tooling-and-protection.md) — Claude Skills fit assessment, copyright/trademark/business protection.
- [`case-study-04-how-people-arrive.md`](./case-study-04-how-people-arrive.md) — how an audience for original IP actually gets built: the three growth archetypes (and which are closed), a ranked channel list, the owned-vs-rented answer, and site discovery.

Full annotated research (raw technique lists, studio-by-studio notes, complete source lists) lives in the session transcript that produced these files; each case study keeps a trimmed, primary-source list at its own end.
