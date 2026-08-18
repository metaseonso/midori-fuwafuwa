# Midori Fuwafuwa™ — Studio Site

Read [PROJECT.md](PROJECT.md) first for full studio context, then
[BUILD_PLAN.md](BUILD_PLAN.md) for the website build.

## When the user says "GO"

Start executing **BUILD_PLAN.md, Stage A, Phase 0**, in order, checking off each item as you
complete it. Do not stop to re-derive or re-litigate anything the plan or `knowledgebase/`
already settled — read `knowledgebase/decisions/decision-log.md` if something looks
undecided before asking.

Work straight through Stage A (Phases 0–3: setup, the Dreamland hub, all three dream fields,
the forest cycle) before touching Stage B. Stage B (Cloudflare, SEO, analytics, legal pages) is
explicitly deferred — the founder wants the UX nailed first. Do not start it unprompted.

## Required reading before writing any code

| File | Why |
|---|---|
| `BUILD_PLAN.md` | The actual task list, staged, with guardrails and done-conditions |
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

`.claude/skills/` — 8 official GreenSock GSAP skills, `scroll-experience`, `accessibility-auditor`,
`zajno-motion`. All inspected and safe. Use them; don't reinstall or re-verify.
