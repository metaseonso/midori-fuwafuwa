---
title: "Website Build Plan"
date: 2026-08-19
status: ready to build — UX first, business wiring deferred
audience: a fresh build session — self-contained, no re-derivation needed
---

# Website Build Plan

## Read these first

| File | Why |
|---|---|
| `brand/DESIGN_SYSTEM.md` | The palette, type, spacing, motion tokens. **§7 is copy-pasteable CSS.** |
| `knowledgebase/craft/the-dreamland.md` | The site concept and the navigation model |
| `knowledgebase/craft/crawlers-and-parallax.md` | **The build rules. Read before writing the hub.** |
| `knowledgebase/INDEX.md` | Everything else |

**Do not re-litigate settled decisions.** `knowledgebase/decisions/decision-log.md` has each one with
its reasoning.

---

## What we are building, and in what order

A studio site for **Midori Fuwafuwa™**. Its job is **building an audience for the studio's original
IP**. It is where people **get to know** the productions — not where they use them.

**The feeling is ふわふわ — soft, floaty, weightless, drifting.** No architecture, no furniture, no
hard edges. Soft layered depth. The mascot is a cloud; the site should feel like the inside of that
character.

**Movement:**
1. **Scroll** to drift through the Dreamland
2. **Click** to enter a dream field (one production)
3. **Scroll deeper** within a field to reach its forest

**Order of work, deliberately staged (2026-08-19):**

> **Nail the UX first. Wire up the business layer after.**
> **"Exploring the dreamworld is the focus" — the founder, 2026-08-19.**

Stage A builds and proves the feel on GitHub Pages, free and simple, with nothing to configure.
Stage B — once the UX is right — migrates hosting to Cloudflare and adds everything that makes the
site real for the outside world: analytics, legal notices, search visibility. This split exists
because none of Stage B's decisions should shape Stage A's design work, and none of them need to be
made before there's something worth looking at.

**Two things narrow Stage A further, per the founder's direction:**

1. **All three productions are dream fields in Stage A**, each with the content already given
   during intake — not just The Kits. The Dreamland is the thing being explored; it needs more than
   one field to actually feel explorable.
2. **The Forest's consolidation cycles (monthly sapling, seasonal grove) are UX to build now** — as
   their own self-contained, interactive thing, seeded with fixture data. **Explicitly do not wire
   this to GitHub Activity, Whimsy, or any real pipeline in Stage A.** That connection is separate,
   later work — see "Not in this build." What's needed now is the feeling of a forest that has grown
   through real cycles, which fixture data can express just as well as live data can.

---

## Stack

| | Stage A (now) | Stage B (later) | Why |
|---|---|---|---|
| **Framework** | **Astro**, `output: 'static'` | unchanged | Everything prerendered. Content Collections fit the Forest manifest pattern |
| **Host** | **GitHub Pages** | **Cloudflare Pages** | GH Pages: zero setup, free, deploys straight from the repo — right for UX iteration. Cloudflare: decided for the real launch, rebuilds on push, pairs with cookieless analytics |
| **Repo** | **GitHub**, public or private, your call | same repo | Needed either way — the Forest pipeline reads it later regardless |
| **Analytics** | none | Cloudflare Web Analytics | Nothing to measure yet; adding it now would just be noise during design iteration |
| **Motion** | Native CSS scroll-driven animation primary; GSAP + Lenis only where CSS can't express it | unchanged | Compositor-only. See `efficient-motion.md` |
| **Fonts** | Baloo 2, Nunito, Gowun Dodum, Caveat — self-hosted OFL | unchanged | Self-hosting from day one avoids ever touching Google Fonts |

**The guardrails below apply in both stages.** They are about the site working, not about who's
hosting it.

---

## 🔴 Guardrails — violating any of these breaks the site

These are documented failure modes, not preferences. Full reasoning in `crawlers-and-parallax.md`.
They apply from the first commit — retrofitting them later is much more expensive than building with
them from the start.

1. **Cap every fullscreen element.** `min-height: 100svh; max-height: 900px;`
   Googlebot expands its viewport to full page height. An uncapped `100vh` hero balloons to
   thousands of pixels and starves everything below it. **This is the single most likely way this
   specific site fails.**

2. **Content exists in the HTML. Animation only animates.**
   Googlebot never scrolls. No AI crawler runs JavaScript at all. Never
   `onEnter: () => injectSection()`.

3. **Never `client:only`** on anything containing content. Use `client:visible` — same server HTML,
   deferred hydration.

4. **Hide only when JS is present:**
   ```html
   <script>document.documentElement.classList.add('js')</script>
   ```
   ```css
   html.js .reveal { opacity: 0; transform: translateY(24px); }
   @media (prefers-reduced-motion: reduce) {
     .reveal { opacity: 1 !important; transform: none !important; }
   }
   ```
   No-JS clients and GSAP failures must still show content.

5. **`transform` and `opacity` only.** Nothing that touches layout.

6. **Every JS/CSS chunk under 2 MB uncompressed.** Googlebot truncates at 2 MB per resource →
   syntax error → blank render. Split GSAP/Lenis into separate chunks; check `dist/_astro/*.js`.

7. **Real `<a href>` to real prerendered URLs.** No hash routing.

8. **No localStorage gating.** Googlebot clears storage between loads — an intro splash gated on
   "seen it" hides the site from Google permanently.

9. **Reduced motion is designed first**, not bolted on. The static state is the primary design.

10. **Stable image URLs across deploys.** Hashing filenames every build re-mints every URL and
    restarts Google's discovery. Matters even on GitHub Pages, so build the habit now.

---

# Stage A — UX

Everything here is about how the site feels. No analytics, no legal pages, no host-specific
configuration beyond "it's live and shareable."

## Phase 0 — Setup

- [ ] `npm create astro@latest` — static output, TypeScript optional
- [ ] GitHub repo, first commit
- [ ] `@astrojs/sitemap` (harmless now, ready for later)
- [ ] Paste `DESIGN_SYSTEM.md` §7 tokens into `src/styles/tokens.css`
- [ ] Self-host the four fonts as WOFF2, subset. `font-display: swap` for Baloo 2, `optional` for
      Caveat
- [ ] Enable GitHub Pages (Settings → Pages → deploy from `gh-pages` branch or GitHub Actions)
- [ ] Add a GitHub Actions workflow: build Astro → deploy to Pages, on every push to `main`

**Done when:** an empty styled page is live at the `github.io` URL, and `curl` returns real HTML.

---

## Phase 1 — The Dreamland hub

The front door. Drift through soft layered depth; dream fields appear as you move.

- [ ] **Design the static frame first.** A single still cloudscape with the mascot. If it is not
      beautiful motionless, motion will not save it
- [ ] Layer art as separate transparent PNG/SVG: far → mid → subject → near → foreground.
      **Five layers maximum**
- [ ] Parallax via `animation-timeline: scroll()` with `animation-range`
- [ ] `@supports (animation-timeline: scroll())` guard → **static fallback, not a JS polyfill**
- [ ] Cap every fullscreen element (Guardrail 1)
- [ ] Field entry points in the HTML as real `<a href="/fields/…">`
- [ ] Reduced-motion: layers hold at rest, ambient loops stop

**Done when:**
- `curl -A "GPTBot" <url> | grep -c "<img"` returns every image
- DevTools at 1024 × 8000, hard reload, no scroll — nothing is missing or stuck invisible
- `prefers-reduced-motion` gives a complete still image
- Lighthouse ≥ 95 on a mid-range mobile profile

---

## Phase 2 — All three dream fields

**Every production gets a field now**, built from the content already gathered during intake. The
Dreamland needs more than one field to be worth exploring.

| Field | Content source | Note |
|---|---|---|
| **The Kits** | `productions/the-kits/PROJECT.md` + `reference/` | Flagship IP. Fullest content — build this one first as the template |
| **Whimsy** | `productions/whimsy-fairy-journal/PROJECT.md` + `reference/` | Second-fullest. The fairy, the journal-world premise |
| **Couple App** | `productions/couple-app/PROJECT.md` | **No name, no reference art.** See below |

- [ ] `/fields/the-kits`, `/fields/whimsy`, `/fields/couple-app` — each its own prerendered page
- [ ] Entry transition from hub → field. `transform`/`opacity` only. Sinking in is the obvious move
- [ ] Field content: the production's own characters (not the studio personas — see the two-layer
      rule in `PROJECT.md`)
- [ ] Production accent tint over the studio palette. **The studio system always wins**

**Couple App — an unformed dream, not a placeholder apology.** It has no name and no art yet, and
that is fine to build *as* a field: represent it as a dream still taking shape — mistier, less
resolved, fewer details in focus than the other two — rather than a "coming soon" notice. This fits
the Dreamland concept directly rather than working around a content gap. Replace it with real
content the moment the founders give it.

**Done when:** all three fields work standalone at their own URLs, and each is reachable by clicking
from the hub.

---

## Phase 3 — The forest within: consolidation cycles as UX

**Build the cycle itself, not just a renderer for someone else's data.** The forest should visibly
show a monthly sapling and a seasonal grove — the studio's actual rhythm — as something a visitor
can explore and understand, seeded with fixture data written now.

⚠️ **Explicitly standalone in Stage A.** Do not wire this to GitHub Activity, a Claude synthesis
call, or Whimsy. That connection is separate, later work (see "Not in this build"). What Stage A
needs is the *feeling* of a forest that has grown through real cycles — which fixture data expresses
just as well as live data, and is far cheaper to iterate on while the UX is still moving.

- [ ] Astro Content Collection reading `productions/<slug>/recaps/*.json`
- [ ] **One generic `<Scene>` component** iterating `scenes[]`. A new month must never touch code —
      only data. This discipline matters even with fixture data, because it's the same component the
      real pipeline will feed later
- [ ] **A monthly sapling and a seasonal grove as distinct, visible states** — not just a flat list of
      recaps. A grove should read as "more grown" than a single sapling; the difference should be
      felt, not just labelled
- [ ] Reveal via `animation-timeline: view()`
- [ ] Each scene: one real asset, prose, mood tag, source link (a placeholder link in Stage A —
      there's no real PR/issue yet)
- [ ] A graceful empty state for productions with no recap history yet — likely all three at first
- [ ] **Write fixture manifests for all three productions**, spanning a few months and at least one
      full season, using the content already gathered in each `PROJECT.md`. This is writing work, not
      just test data — treat it as the first real drafts of what the forest says

**Done when:** each field's forest shows a believable history — several saplings, at least one
grove — built entirely from fixture data, and dropping a new hand-written JSON manifest into the
folder renders a new sapling with no code changes.

---

## Stage A verification

Run this before calling the UX done, whether or not Stage B has started:

- [ ] `curl -A "GPTBot"` on every page — a human should be able to read it from raw output alone
- [ ] Google's own scroll-diff script — `lazyimages_without_scroll_events.js` from
      GoogleChromeLabs/puppeteer-examples. **The best automated check for a parallax site**
- [ ] Expanded-viewport simulation: DevTools custom device 1024 × 8000, hard reload, no scroll
- [ ] Reduced-motion pass on every page
- [ ] Keyboard navigation and visible focus states — **not yet specified anywhere; decide this during
      build, don't skip it**

**Still a creative call — decide during Stage A:**

- **Is it clouds?** The most natural reading of fuwa fuwa, and the best parallax fit — but only one
  interpretation. Worth sketching before committing.
- **Where do the fields sit** — below, through gaps, further along? This decides whether drifting is
  vertical, horizontal, or into depth.
- **Does the mascot accompany you?** Must survive reduced motion and the motion budget.
- **What the visitor sees labelled.** "Dream field" and "forest" are internal vocabulary. External
  copy is undecided.
- **Where the personas hand over.** Studio level is Seonso and Grumpy Carrot; each field belongs to
  its production's characters.

---

# Stage B — Wiring it up for business

**Do not start this until the UX from Stage A feels right.** Everything here is infrastructure and
disclosure, not design — it should slot on top of a finished feel, not shape it.

## Phase 4 — Move to Cloudflare

- [ ] Connect the repo to Cloudflare Pages
- [ ] **⚠️ Check Cloudflare AI-bot settings immediately on setup.** Setting Training to "Block on all
      pages" **also blocks Googlebot.** Use managed robots.txt, not the blunt toggle
- [ ] Point the domain at Cloudflare once registered (`midorifuwafuwa.com` or `.studio` — see
      `PROJECT.md`)
- [ ] Retire the GitHub Pages deploy once Cloudflare is confirmed working, or keep both — GitHub
      Actions can deploy to Cloudflare Pages too

## Phase 5 — Search and discovery

- [ ] `public/robots.txt` — allow search + AI-search crawlers, disallow training crawlers. Template
      in `crawlers-and-parallax.md`
- [ ] `ImageObject` licence metadata + IPTC embedded on every artwork — see
      `knowledgebase/site/seo-and-discovery.md`. **The highest-value markup on the site**
- [ ] `Organization`, `WebSite`, `BreadcrumbList`, `ProfilePage` structured data — see
      `seo-and-discovery.md` for exactly what's still live vs. deprecated
- [ ] **Verify in Google Search Console.** It backfills nothing; data before verification is lost
      permanently
- [ ] Whitelist `Google-InspectionTool` in Cloudflare or URL Inspection goes dark

## Phase 6 — Analytics

- [ ] Enable Cloudflare Web Analytics
- [ ] **Check whether the dashboard shows UTM parameters** — if not, either accept the gap or move to
      Plausible ($9/mo), and lean on per-channel landing pages regardless (`measuring-arrival.md`)

## Phase 7 — The small pages and legal notices

- [ ] `/ethos` — **the founder's own words from `ETHOS.md`. Do not rewrite in a corporate or AI
      voice**
- [ ] `/privacy` and `/terms` — copy is written verbatim in
      `knowledgebase/site/privacy-policy-text.md`. One screen each
- [ ] Footer: `© 2026 Midori Fuwafuwa Studio™. All rights reserved.`
- [ ] Contact: a plain `mailto:` link. **No contact form**
- [ ] Per-channel landing pages: `/hello-bluesky`, `/from-the-newsletter`, `/zine`

## Phase 8 — Final verification

- [ ] Repeat the Stage A verification pass on the live Cloudflare domain
- [ ] URL Inspection → Test live URL → rendered HTML. Every `<img src>` present, `<h1>` present,
      nothing stuck at `opacity: 0`
- [ ] Verify the served `robots.txt` matches `public/robots.txt` (Cloudflare can override it)

---

## Skills to use

- **`scroll-experience`** (installed) — parallax and scroll-driven patterns
- **`greensock/gsap-skills`** (installed) — official GSAP reference; `gsap-scrolltrigger` and
  `gsap-performance` specifically
- **`claude-api`** (bundled) — for Phase 3's structured output, when the real pipeline gets built

⚠️ Neither scroll skill covers **native CSS scroll-timeline** or **`prefers-reduced-motion`**, which
this build treats as primary. Use them for the GSAP layer only; the CSS layer is governed by
`efficient-motion.md`.

---

## Not in this build

- **Whimsy and the Couple App** live on their own infrastructure. They collect private personal data;
  the site collects nothing. **Never share a privacy policy, domain surface, or architecture.**
- **The AI reception** — recommended to ship on Whimsy's infrastructure rather than build twice.
  Launch with the `mailto:`.
- **The real Forest pipeline** (GitHub Action → Claude synthesis → manifest, wired to actual repo
  activity). Phase 3 builds the cycle's UX and renderer against fixture data on purpose — the
  generator that produces *real* manifests comes later, once there's real repo activity to narrate.
  Swapping fixture manifests for generated ones should require no component changes, by design.
- **Any connection to Whimsy.** The engine is shared conceptually (see
  `research/synthesis-cross-findings.md`), but that is a future architecture decision, not something
  Stage A needs to wire up. Treat the studio's own Forest as fully standalone.
