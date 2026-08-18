# Midori Fuwa Fuwa

## What it is
A production studio.

## Who runs it
Seonso and Grumpy Carrot.

## Setting
Based out of a Dreamland. Seonso and Grumpy Carrot share this Dreamland.

## Brand
Official logo: `brand/logo/midori_fuwafuwa_logo_official.png`
Mascot: a small fluffy mint-green cloud creature. It paints at a tiny easel.

## Two layers: personas and creations

The studio runs on a deliberate two-layer structure. Keep them distinct in all art,
copy, and site architecture:

1. **Artist personas** — **Seonso** (fox sage) and **Grumpy Carrot** (bunny). These are the
   founders' own avatars. They front the *studio*.
2. **Created characters** — the characters those personas author inside each production. In
   The Kits, that includes a fox father and a fox mother.

A persona and the character it creates may closely resemble each other (Grumpy Carrot the
bunny → the fox mother; Seonso → the fox father). That resemblance is intentional and has an
in-world reason, held for later.

**Site consequence:** the studio level (hub, front page, mascot interactions) belongs to the
personas. Inside a production's Field, the production's own characters lead. Do not mix the
two layers in one frame without a reason.

## Characters

### Seonso (선소)
Files: `brand/characters/seonso/`
- Fox sage. Artist. Dreamer.
- Look: black hair in a bun, black-and-gold outfit, spiral (선소) motif.
- Vibe: calm, mindful, drinks tea, thinks in spirals not lines.
- Companion: a white fox spirit.

### Grumpy Carrot
Files: `brand/characters/grumpy-carrot/`
- Bunny girl. Artist. Dreamer. Carrot devil.
- Look: brown curly hair, carrot-shaped hair clips, pink-and-black outfit, bunny ears.
- Vibe: loves drawing cute things, hates boring days, runs on coffee and chaos, secretly a softie.
- **Official file:** `grumpy_carrot_ref_sheet_corrected.jpeg` — mug text "I HATE MONDAYS" removed
  (blank pink mug, cat logo intact). This is the approved reference.
- Original file `grumpy_carrot_ref_sheet.jpeg` kept for history only, not for use.
- Correct catchphrase for Grumpy Carrot is **"I LOVE CHOCOLATE."** (not "I hate Mondays").

### Together
Files: `brand/characters/together/`
- Seonso and Grumpy Carrot shown together.

## Productions
- **01 — The Kits** (`productions/the-kits/`) — original IP, starting as a children's book
  series. Seonso and Grumpy Carrot's children exploring the many worlds around us. First
  production, and the primary subject of the website.
- **02 — Whimsy** (working title, `productions/whimsy-fairy-journal/`) — a product. A fairy
  keeps your journals, notes and doodles, and turns them into an explorable world with
  seasonal personalised story recaps. **Shares the Forest pipeline architecture** from
  Case Study 02 — confirmed by the founders: the website's own update cycle *is* Whimsy's
  skeleton, and Whimsy is that skeleton offered to the world as a product.
- **03 — Couple App** (name TBD, `productions/couple-app/`) — "very us." Rooted in the
  founders' own relationship. Likely a third front-end onto the same narrative engine.

## The rhythm — one clock on every level

The monthly and seasonal cadence in the website plan is **not an arbitrary schedule.** The
founders align it deliberately across every layer of the studio:

- **Natural seasons** — four.
- **Agricultural cycles** — planting, growing, harvest, rest.
- **Business cycles** — four quarters map onto four seasons.
- **Website cycle** — a sapling per month, a grove per season (the Forest).
- **Product cycle** — Whimsy's seasonal personalised recaps run on the same clock.

This is why the site vocabulary is pastoral — **Field, Forest, sapling, grove.** Those words
encode the studio's actual operating rhythm; they are load-bearing, not decorative.

**Consequences to hold onto:**
- Seasonal variation is a first-class mechanism in the design system, not a seasonal promo.
- The Forest's clock and the studio's business clock are the same clock. Building one exercises
  the other.
- Whimsy sells that rhythm outward. The studio has to actually live it for the product to be
  honest.

## Website — direction (research phase)

**The site is for the production studio. Period.** (Confirmed 2026-08-19.) It is Midori
Fuwafuwa's own site — not The Kits' site, not Whimsy's. Productions appear as Fields within it;
the subject is the studio.

**Purpose:** building an audience for our original IP. Per Case Study 01 this sets the
positioning — personas, world, and return-visit hooks lead; client-portfolio depth and sales
framing do not.

**Scope — settled 2026-08-19. The site is where people GET TO KNOW the productions. It is not
where they USE them.**

An introduction, not a venue. Consequences:
- **No product functionality lives on the site.** Whimsy and the Couple App are used elsewhere,
  on their own infrastructure.
- **The site collects nothing.** No accounts, no forms, no tracking cookies. Contact is a plain
  `mailto:` link, so nothing reaches our server. See [[knowledgebase/site/collect-nothing]].
- **AI reception decided in principle** — recommended to ship on Whimsy's infrastructure rather
  than build twice. See [[knowledgebase/site/contact-without-collecting]].
- **The products carry their own legal footing entirely.** They hold private personal data; the
  site does not. Never let the two share a privacy policy, a domain surface, or an architecture.
- This keeps the studio site permanently cheap, fast, and near-obligation-free — which is what
  makes the "collect nothing" model hold as the productions grow.

### Standing notice convention — apply everywhere applicable
- **™** after "Midori Fuwafuwa" wherever the name appears as a brand: site header and footer,
  book copyright pages, app store listings, social profiles, decks, merchandise.
- **©** notice in the site footer: `© 2026 Midori Fuwafuwa Studio™. All rights reserved.`
- **Never ®** until a registration actually issues, and then only in the country where it issued.
- Full reasoning: [[knowledgebase/site/site-notices]] · checklist:
  [[knowledgebase/legal/trademark-launch-checklist]]

### Internal structure
**Midori Fuwa Fuwa, and exploring the different dream fields (products).**

Internal structural labels only — external labelling depends on the creative design, undecided.

```
Midori Fuwa Fuwa (studio)
└── dream fields — one per production
    ├── The Kits
    ├── Whimsy
    └── Couple App
```

**Hosting:** Cloudflare. **Domain:** `midorifuwafuwa.com` or `.studio`, not locked.

## Ethos
See [[ETHOS]] — the founder's own words. Not to be rewritten in a corporate or AI voice.

## 🔨 Build
**[[BUILD_PLAN]]** — the website build plan. Self-contained; a fresh session can execute it without
re-deriving anything. Read it before starting work on the site.

## 📚 Knowledgebase

**Start at [[knowledgebase/INDEX]].** Atomic notes, wikilinked, Obsidian-ready. Legal, site
policy, craft technique, and a dated [[knowledgebase/decisions/decision-log|decision log]].

Long-form source research stays in `research/`.

**Style — settled 2026-08-19. There is ONE Midori Fuwafuwa reference image:**

```
brand/logo/midori_fuwafuwa_logo_official.png
```

That image is the entire design language of the production site. Nothing else feeds it.

- **The artist personas each have their own distinct style, deliberately.** Seonso and Grumpy
  Carrot established the studio and work in it, but their reference sheets record *their* styles,
  not the studio's. Their palettes live in `brand/characters/PERSONA_PALETTES.md` and are **not**
  studio tokens.
- **Production reference images are vision anchors** for their own productions — mood, world,
  composition. Not studio style references.

Full system: `brand/DESIGN_SYSTEM.md`.
Files: `research/` — **`research/README.md` is the reference document; start there.**
Value principles: immersive and informative, yet minimalist. Cute, fluffy, chibi as the
intended visual outcome. Snappy to render; assets simple to produce in one consistent
design language.
Terminology: a **Field** is one production's own open, explorable diorama space (2D/2.5D
layered parallax, replaces the earlier "room" idea). A **Forest** is that production's
living, auto-updating continuity layer — grows a sapling per monthly consolidation, a
grove per season, sourced from real GitHub activity.
- Case Study 01: efficient (non-resource-intensive) parallax/immersive technique research,
  studio showcase patterns, and a proposed fusion — each production as its own Field,
  mascots performing the studio's personality instead of copy.
- Case Study 02: research on auto-consolidating production continuity straight from GitHub
  activity on a monthly + seasonal clock (no manual redesign) — the Forest behind each
  Field — an honest novelty assessment, and a proposed five-stage reference architecture.
- Case Study 03: Claude Skills fit for building this (official + community, priority-ranked,
  overlaps/disqualifications noted) and copyright/trademark/business-protection research
  for an original-IP studio with mixed hand-drawn/AI-assisted art.

## Intake log
- 2026-08-18: Studio identity and logo confirmed.
- 2026-08-18: Character reference art for Seonso and Grumpy Carrot sorted. Noted mug text
  correction: "I HATE MONDAYS" → "I LOVE CHOCOLATE."
- 2026-08-18: Mug text removed from Grumpy Carrot's ref sheet by pixel edit (cat logo
  preserved). `grumpy_carrot_ref_sheet_corrected.jpeg` approved as the official file.
- 2026-08-18: Website research phase started — two case studies (efficient immersive
  showcase; living GitHub-driven pipeline) added under `research/`.
- 2026-08-19: Website audience confirmed — building an audience for original IP.
- 2026-08-19: Production 01 "The Kits" added — children's book series IP.
