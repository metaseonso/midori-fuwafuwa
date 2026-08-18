---
title: Decision log
tags: [decisions, index]
status: living
updated: 2026-08-19
---

# Decision log

Settled calls with their reasoning, so they don't get re-litigated. Newest first.

---

## 2026-08-19

### Stage A scope widened: all three fields, plus the consolidation cycle itself
*"Right now all the productions are a field area with some content. I gave you that content. So
exploring the dreamworld is the focus of the UX."* Two changes to `BUILD_PLAN.md` Phase 2/3:
(1) all three productions get a field in Stage A, built from intake content already gathered — not
just The Kits; Couple App (no name, no art yet) is represented as an unformed dream rather than a
placeholder. (2) The Forest's monthly/seasonal consolidation cycle is built as its own interactive
UX now, seeded with hand-written fixture manifests — explicitly **not** wired to GitHub Activity or
Whimsy in Stage A. That wiring is separate, later work.

### Build order: UX first on GitHub Pages, business wiring later on Cloudflare
Split the build plan into **Stage A** (Astro on GitHub Pages — hub, one field, the forest renderer,
no analytics, no legal pages, no host config) and **Stage B** (migrate to Cloudflare, add search
markup, analytics, privacy/terms, robots.txt). Rationale, founder's own words: *"for now I want to
nail down the UX. Then we can wire it up for business."* The guardrails (100vh cap, content-in-HTML,
reduced-motion-first, etc.) apply from commit one in both stages — retrofitting them later is far
more expensive than building with them. → `BUILD_PLAN.md`

### Site concept: the Dreamland, fuwa fuwa — not a studio
*"I like the fuwa fuwa feel more than the studio feel."* An earlier concept ("The Easel") made the
logo literal — a studio interior, the mascot at its easel, canvases as fields. **Retired.** A studio
is architecture and furniture; that is the opposite of ふわふわ. The logo keeps the easel as the
studio's *mark*; the world does not have to match the mark.
→ [[../craft/the-dreamland]]

### Navigation: scroll to wander, click to choose
*"Scroll through the dream world, explore a field, see the forest within."* Three levels — drift
the hub by scrolling, enter a field by clicking, go deeper within it to reach the forest. Survived
the concept change intact, because it describes movement rather than scenery.

### The Forest moved inside the Field
Earlier research placed it at the *edge*. "Within" is better: depth becomes the reward for
curiosity, the front of each field stays calm, and the metaphor holds — a forest inside a field is
somewhere you walk into. → [[../craft/field-and-forest]]

### Channel strategy: build the small thing you control
Every social acquisition window in the research has closed and most closings can be dated. **Do:**
a seasonal letter (Buttondown, no tracking), a shop that exists before traffic, Reddit twice a year,
Instagram monthly for legibility not growth, RSS→Bluesky free. **Don't:** Webtoon/Tapas, Substack,
TikTok/YouTube, Discord, any daily cadence. → [[../channels/channel-overview]]

### The grove can be the publication; the Forest cannot be the publisher
Auto-generated process content fails on audience fit, a measured 31%-vs-7% trust penalty against
perceived-AI content, and Google's scaled-content-abuse policy. Fix: a **~2 hour editorial pass per
season**, which doubles as the human-authorship pass.

### Staleness convention adopted
Research notes carry `verified:` and `staleness:` frontmatter plus a warning banner. Anything with a
date in it is a snapshot, not a standing fact.

### Hosting: Cloudflare
"Cloudflare is the go to." Pairs directly with the already-decided Cloudflare Web Analytics, and
Cloudflare Pages rebuilds on git push — which is exactly what the
[[../craft/field-and-forest|Forest]] pipeline needs with no extra plumbing.

### Domain: `midorifuwafuwa.com` or `.studio` — not locked
Founder's note: fine if it ends up being something different later. Not important right now.
⚠️ One dependency: check availability **and** trademark clearance together before committing, since
the mark and the domain should match. → [[../legal/trademark-launch-checklist]]

### Internal structure: studio → dream fields
**"Basically it's Midori Fuwa Fuwa and exploring the different dream fields (products)."**

These are **internal structural labels**, not front-end copy. External labelling depends on the
creative design, which is not decided.

```
Midori Fuwa Fuwa (studio)
└── dream fields — one per production
    ├── The Kits
    ├── Whimsy
    └── Couple App
```

"Dream field" reconciles the two existing terms: Dreamland (the shared setting) + Field (one
production's explorable space). → [[../craft/field-and-forest]]

### Sitemap: deferred, deliberately
Depends on the creative design. The structural model above is settled; the page list is not.

### Ethos: founder's own words only
Written as arranged direct quotes, with raw source quotes preserved beneath. Explicit instruction:
*"don't make it an AI statement. keep my words. its human and simple."* → `ETHOS.md`

### Knowledgebase organised for Obsidian
Atomic notes, wikilinks, `knowledgebase/` folder with an [[../INDEX|INDEX]] as the map. Rationale:
the project's surface area grows as productions are added, and long documents stop being navigable.
Replaces the root-level `SITE_NOTICES.md` and `ANALYTICS.md`, whose content moved here.

### No YouTube embeds
An embedded YouTube player drops a tracking cookie on page load, before anyone presses play — which
would force a consent banner onto an otherwise cookie-free site. If video is ever needed:
click-to-load poster, or `youtube-nocookie.com`. → [[../site/cookie-traps]]

### Analytics: Cloudflare Web Analytics. Google Analytics rejected.
Free, cookieless, no banner needed. Google uses cookies, forces a banner, loses declining visitors
from the numbers anyway, and carries EU data-transfer friction. → [[../site/analytics-without-cookies]]

### Contact: AI reception + email
Decided in principle. Recommendation on sequencing: **launch with a `mailto:` only, add the AI
reception on Whimsy's infrastructure** — it is the same technology at 1% scale, and Whimsy's privacy
architecture decision covers both. Architecture still open. → [[../site/contact-without-collecting]]

### Collect nothing
No accounts, no forms, no tracking cookies. Founding principle, and a stance rather than only a
compliance strategy: *"Happy to be reached out to vs us trying to track everything."*
→ [[../site/collect-nothing]]

### Site scope: introduction, not venue
The site is where people **get to know** the productions, not where they **use** them. No product
functionality on it. Products carry their own separate infrastructure and legal footing.

### Founder is US-based → USPTO is the office of origin
Confirmed. Sets the trademark path. → [[../legal/madrid-protocol]]

### Global selling, tiered registration
Selling worldwide needs no registration. Registering all ~115 Madrid members would cost tens of
thousands to protect markets with no sales. Instead: one Madrid filing designating **EU · UK · Japan
· South Korea · China · Canada · Australia.** → [[../legal/madrid-protocol]]

### ⚠️ China registered early, not "as we grow"
First-to-file, and squatting is an organised industry there. Merchandise manufacturing alone is
reason enough. Founder's assessment: *"really annoying and stupid"* — agreed, and complied with
early anyway because recovery later costs orders of magnitude more.
→ [[../legal/china-first-to-file]]

### ™ now, ® never until registration issues
™ is free, needs no registration, and is understood internationally. ® without a registration is
improper and penalised in some countries. → [[../legal/trademark-is-territorial]]

### AI-made art is accepted
It does not have to be human-made. The earlier copyright concern was framed too narrowly: a book is a
human-authored compilation, the text is fully protected, characters are protected across a body of
work and by trademark, and arrangement is protectable even when components are AI-generated. Effort
goes to **writing and trademark**, not image paperwork. → [[../legal/ai-made-art-and-copyright]]

### Whimsy age floor: 13+
Deliberately set to stay out of COPPA. Revisit with a parental-consent flow only if genuine demand
appears from younger users. Rationale: keep compliance burden low so studio energy stays on making
things.

### Whimsy audience and interaction model
**Non-tech-savvy people.** An AI they just message, in plain language. No folder trees, no tagging
UI. The fairy *is* the interface. Platform (app vs Telegram vs other) still open — research pending.

### Style: ONE Midori Fuwafuwa reference image
`brand/logo/midori_fuwafuwa_logo_official.png` is the entire design language of the production site.
The artist personas each have their own distinct style, deliberately — their ref sheets are **not**
studio style references, and their palettes live separately in
[[../../brand/characters/PERSONA_PALETTES|PERSONA_PALETTES.md]]. Production reference images are
**vision anchors** for their own productions only. → [[../../brand/DESIGN_SYSTEM|DESIGN_SYSTEM.md §0]]

### Design system derived, v2
15 colours, all sampled programmatically from the logo. Every contrast ratio computed. `--mint` and
Whimsy's lavender **fail as text** and are decoration only; derived deep variants exist for text.
All four seasonal accents are logo colours rotated — no new hue enters the system.

### Website purpose: build an audience for original IP
Not client acquisition, not recruitment, not merchandise-first.

### Two-layer character structure
**Artist personas** (Seonso, Grumpy Carrot) front the studio. **Created characters** live inside
productions. Resemblance between a persona and its created character is deliberate, with an in-world
reason held for later.

### The rhythm is one clock on every level
Natural seasons, agricultural cycles, business quarters, the site's Forest, and Whimsy's recaps all
run on the same monthly/seasonal clock. Pastoral vocabulary encodes it.
→ [[../craft/field-and-forest]]

## 2026-08-18

### Grumpy Carrot mug text removed by pixel edit
"I HATE MONDAYS" was inaccurate; correct catchphrase is "I LOVE CHOCOLATE." Removed the text
entirely rather than typesetting a replacement. Cat logo preserved.
`grumpy_carrot_ref_sheet_corrected.jpeg` is the approved file.

### Studio identity and logo confirmed
Midori Fuwafuwa: a production studio run by Seonso and Grumpy Carrot, out of a shared Dreamland.
Official logo set.

---

## Parked

| Item | Note |
|---|---|
| Founders' / IP agreement | Founder will handle. Shape recorded in [[../legal/joint-authorship-and-credit]]. |
| Money model | Explicitly parked by the founders. |
| Full WCAG AA beyond motion | Keyboard nav, focus states, alt-text discipline not yet specified. |
