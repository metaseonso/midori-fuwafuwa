# Midori Fuwafuwa™ — Studio Site

Read [PROJECT.md](PROJECT.md) first for full studio context, then
[BUILD_PLAN.md](BUILD_PLAN.md) for the website build.

## When the user says "GO"

**Read [OG_REVIEW.md](OG_REVIEW.md) first.** Stage A was built once and audited. The next step is
**not** to restart from Phase 0; it is to *finish* the existing site in the order set out in
OG_REVIEW.md §3 ("Order of work"). Step 1 is the founder approving the storyboard
(https://claude.ai/artifact/CXSsd4HTGzVZaZTuCiTpp4). Do not build hub design work before that
approval. Step 2 (the verification harness against the **built** site) comes before any design
work.

All guardrails in `BUILD_PLAN.md` and `knowledgebase/craft/` still apply. Read
`knowledgebase/decisions/decision-log.md` if something looks undecided before asking.

Stage B (Cloudflare, SEO, analytics, legal pages) is explicitly deferred. The founder wants the
UX nailed first. Do not start it unprompted.

## Required reading before writing any code

| File | Why |
|---|---|
| `OG_REVIEW.md` | **Start here.** The vision in one page, what went wrong in past builds, the architecture and order of work for finishing |
| `BUILD_PLAN.md` | Guardrails and done-conditions (its sequencing is superseded by OG_REVIEW.md) |
| `brand/DESIGN_SYSTEM.md` | Palette, type, spacing, motion tokens — §7 is copy-pasteable CSS |
| `knowledgebase/craft/the-dreamland.md` | The site concept and navigation model |
| `knowledgebase/craft/crawlers-and-parallax.md` | **Hard build rules.** Read before writing the hub — violating these breaks the site for Google and every AI crawler |
| `knowledgebase/INDEX.md` | Map of everything else |

## Ground rules for this project

- **There is exactly ONE Midori Fuwafuwa style reference:** `brand/logo/midori_fuwafuwa_logo_official.png`.
  The design system is derived from it alone. The artist personas (Seonso, Grumpy Carrot) have
  their own distinct styles — never treat their reference sheets as studio style references.
- **The feeling is ふわふわ — soft, floaty, weightless.** No architecture, no hard edges. See
  `the-dreamland.md`.
- **All content for the three productions was already gathered during intake** — see
  `productions/*/PROJECT.md` and their `reference/` folders. Use it; don't ask for it again.
- **The Forest's consolidation cycles are UX to build now, using fixture data.** Explicitly do
  not wire this to GitHub Activity, a real Claude synthesis call, or Whimsy in Stage A.
- **The site collects nothing** — no accounts, no forms, no tracking cookies. This is a Stage B
  concern (privacy pages, analytics) but the no-forms/no-tracking discipline should hold from
  the first line of code.
- `ETHOS.md` is the founder's own words. Never rewrite it in a corporate or AI voice.

## Skills installed for this project

`.claude/skills/` — all inspected and safe (bundled scripts are read-only). Don't reinstall or re-verify.

- **Lean on these:** `webapp-testing` (verify the *built* site, never dev), `frontend-design`
  (restraint, one orchestrated moment; ⚠️ its "cream background is an AI tell" note does not
  apply here — the cream is sampled from the logo and the brief wins), `astro-transitions`
  (native View Transitions; ClientRouter is being removed), `astro-images`, `astro-perf`,
  `performance`, `core-web-vitals`, `web-quality-audit`, `accessibility-auditor`, `scroll-experience`.
- `astro` bundles a scanner. In this repo run it as
  `node .claude/skills/astro/scripts/astro-scan.mjs site --json` (not the plugin path in its docs).
  It scores static source only — it cannot see the runtime bugs; Playwright on the build can.
- GSAP skills (`gsap-core`, `-scrolltrigger`, `-timeline`, `-performance`, `-utils`) are reference
  only: native CSS scroll timelines are primary; add GSAP only with a written reason.
- Flagged for retirement, pending the founder's call (see OG_REVIEW.md §4): `gsap-react`,
  `gsap-frameworks`, `gsap-plugins`, `zajno-motion`. Don't reach for them.
