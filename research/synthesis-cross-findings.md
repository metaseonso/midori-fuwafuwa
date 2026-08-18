---
title: "Synthesis — what the three case studies say together"
date: 2026-08-18
status: read after research/README.md
---

# Synthesis — cross-findings

The three case studies each answer their own question well. This file holds only what
appears when you read them *against each other* — agreements, connections, and gaps that
are not stated in any single file.

## 1. The same shape repeats three times

Each case study independently lands on the same structure: **the infrastructure is already
solved; the original work is narrow and specific.**

| Case study | Already solved (install it) | Actually original (build it) |
|---|---|---|
| 01 — Fields | Scroll/motion tech (native CSS timelines are free) | Using the Dreamland premise as literal site architecture |
| 02 — Forests | Ingestion, storage, rendering, deploy | Narrative-arc construction + story-relevant asset curation |
| 03 — Tooling | Most skills map to existing official/community ones | Two custom skills: narrative-arc, brand-consistency |

**Implication:** this project is considerably smaller than it looks. It is an integration
job around roughly three genuinely new pieces — not a systems build. Effort should
concentrate there and stay off re-deriving solved layers.

## 2. Two case studies converge on one artifact — and three productions consume it

Case Study 02 concludes the narrative-arc + asset-selection step is the only piece with no
off-the-shelf answer. Case Study 03 independently ranks `skill-creator` at #2 *because* of
that finding.

Read together: **the narrative-arc skill is the single highest-value thing to build in the
entire project.** It is the studio's actual differentiator, and it is the one asset worth
treating as an ongoing craft project rather than a one-time prompt.

### Escalation (2026-08-19 intake): this is a platform, not a site feature

The August 19 intake added three productions, and the same engine appears across them:

| Consumer | Input | Output |
|---|---|---|
| Studio **Forest** (website) | GitHub activity | Seasonal story of the studio's work |
| **Whimsy** (product 02) | Personal journals, notes, doodles | Seasonal personalised storyline |
| **Couple App** (product 03) | Shared relationship data | Almost certainly the same treatment |

The founders confirmed the relationship directly: the website's own update cycle *is* Whimsy's
skeleton, and Whimsy is that skeleton offered to the world as a product.

**This reframes the project.** The narrative engine is not polish on a portfolio site — it is
the studio's core technology, with one internal consumer and two commercial ones. Three
consequences:

1. **The Forest is the prototype, and it is nearly free.** Building it against the founders'
   own public repos develops the engine on real data with no users, no private data, and no
   support burden. It is the cheapest possible R&D environment for the studio's most valuable
   asset.
2. **Effort spent on the engine compounds three ways.** Time on arc construction and asset
   curation is not site work borrowed from product work — it is the same work.
3. **Design the products as skins over one engine.** Two products sharing an engine costs far
   less than two products. This should be an explicit architectural constraint from the start,
   not a refactor discovered later.

### The rhythm is deliberate and shared

The monthly/seasonal clock is not a schedule choice. The founders align it across natural
seasons, agricultural cycles, business quarters, the website's update cycle, and Whimsy's
recap cycle — one rhythm on every level. The pastoral vocabulary (Field, Forest, sapling,
grove) encodes that rhythm rather than decorating it.

Practical effect: **seasonal variation belongs in the design system as a first-class token
layer**, and the Forest's clock is the business clock — exercising one exercises the other.

## 3. The Forest architecture already sits on the strongest legal footing (CS02 × CS03)

Neither file connects this, but they fit together cleanly:

- Case Study 03 finds that AI **generation** of art is not independently protectable, while
  human **selection, arrangement, and sequencing** of existing work *is* protectable — and
  that curated selection of real human-made assets is a far safer category than generated
  imagery.
- Case Study 02's Forest pipeline does exactly and only that: it **selects and sequences
  real, already-committed art**. It never generates art.

So the pipeline lands on the safest available footing by construction, not by accident of
caution. Worth preserving deliberately as the design evolves.

**One weak spot to note:** the AI-written *prose* in each recap is AI output, and therefore
thin on protection by the same reasoning. The art and its arrangement are the protected
parts. If a recap's text ever matters commercially, a human editing pass converts it into
human-authored expression.

## 4. The 60-day gotcha has a fix already in hand

Case Study 02 flags that GitHub Actions scheduled workflows auto-disable after 60 days of
repository inactivity, and calls it the one operational risk to design around from day one.
For a two-person studio with bursty work, this will happen rather than might.

The mitigation it recommends — an external trigger calling `workflow_dispatch` — is
available in this working environment directly, via its own scheduled-task mechanism. This
is a solved item, not an open risk, provided it is wired at build time rather than after
the first silent failure.

## 5. Tooling status is ahead of what Case Study 03 assumed

- Priorities **#1 `claude-api`** and **#2 `skill-creator`** are already available in this
  environment. No installation needed.
- Priority **#6** recommended `gsap-scrolltrigger` from the community `freshtechbro` set.
  The **official GreenSock `gsap-skills`** repo is a strictly better source for the same
  need — same dedicated `gsap-scrolltrigger` skill, published by the library's own authors.
  Treat the official one as the reference and the community one as redundant.
- The `mcpmarket/*` skill paths named in early planning do not resolve to a real source and
  should not be used. The equivalent content is in `sickn33/agentic-awesome-skills`
  (`skills/scroll-experience`), verified as instruction-only text.
- Still not present, still worth adding when build starts: `webapp-testing`,
  `frontend-design`, `accessibility-auditor`, `orchestrating-gsap-lenis`.

## 6. Sequencing constraint: the Forest cannot come first

The Forest narrates real GitHub activity on a production's repo. It therefore requires
productions that (a) exist and (b) have live repos accumulating commits and committed art.
Built too early, it produces an empty forest and nothing to demonstrate.

The dependency runs one way: **Field → production activity → Forest.** The Field is
buildable today from existing brand assets; the Forest is gated on real pipeline activity.

## 7. The open question the research does not answer — ANSWERED 2026-08-19

**Answer: building an audience for the studio's original IP.** Not client acquisition, not
recruitment, not merchandise-first.

That settles the positioning per Case Study 01: personas, world, and return-visit hooks lead;
portfolio depth and sales framing do not.

**Scope clarification (founders, same day):** *"the site is for the production studio. Period."*
The site's subject is Midori Fuwafuwa itself. Productions are Fields inside it — not the thing
the site is about. An earlier draft of this file called The Kits "the site's primary subject";
that was wrong and is corrected here.

The original analysis is kept below for the reasoning that produced the question.

### Original framing

All three case studies answer *how*. None states *who the site is for* or what it is meant
to achieve commercially.

This matters concretely, because Case Study 01's clearest finding is that **content depth is
a positioning choice calibrated to audience, not a universal "more is better"** — Immersive
Garden withholds process to protect mystique with luxury clients; Active Theory publishes
deep engineering write-ups to attract technical hires; Cuberto front-loads an FAQ to
pre-empt sales calls. Each is correct for a different audience.

The current plan (minimal front-of-house Field, deep Forest behind it) is a coherent
answer — but it is only *verifiably* the right answer once the audience is named. Candidate
purposes, which pull in noticeably different directions:

- **Attract client work** → portfolio depth and contact path matter most.
- **Build an audience for original IP** → mascots, world, and return-visit hooks matter most.
- **Recruit or attract collaborators** → the Forest's process transparency becomes the lead.
- **Sell merchandise later** → asset licensing and trademark move up the priority order.

Naming this changes what belongs on the front page, how much the Forest is promoted, and
which Case Study 03 protection items become urgent rather than eventual.

## 8. Recommended build order

*Revised 2026-08-19 after the three-production intake. The narrative engine moves up: it is
platform R&D with three consumers, not a late-stage site feature.*

1. **Founders' / IP agreement.** Orthogonal to the build, cheap now, compounding cost later.
   Case Study 03's highest leverage-per-effort item — and it now covers three productions and
   a shared engine, not one website, which raises the stakes of leaving it unwritten.
2. ~~Name the audience~~ — **done.** Building an audience for original IP.
3. **Design system** — in progress. Locks the one consistent visual language the value
   principles demand, before asset production begins on either The Kits or Whimsy.
4. **Brand-consistency skill** via `skill-creator`, built on top of the design system, so every
   later session stays on-palette and on-model without re-explaining.
5. **One Field, end to end** — hub plus The Kits' Field, reduced-motion state designed first.
   Proves the parallax approach at real scale, on the flagship IP.
6. **Narrative-arc skill + the studio Forest, together.** These are one piece of work, not two.
   The Forest is the engine's development environment: real data, public repos, no users, no
   private data, no support burden. This is the studio's core technology getting built in its
   safest possible sandbox.
7. **Whimsy** — the same engine, pointed at private personal data. Gated on the privacy
   architecture decision (local / private cloud / zero-retention API), which must be made
   before build, not after.
8. **Couple App** — a second skin over the Whimsy engine.

**Decisions that block later steps and are cheap to make now:**
- The privacy architecture for personal-data synthesis (blocks 7 and 8).
- One house art style vs. per-production styles (blocks real asset production; The Kits'
  watercolour and Whimsy's rendered CGI references currently disagree).
- Intended age range for Whimsy (COPPA exposure if under-13 users are in scope).
