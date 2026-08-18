---
title: Field and Forest
tags: [craft, architecture, vocabulary, core-concept]
status: settled — core site vocabulary
updated: 2026-08-19
source: research/README.md
---

# Field and Forest

The site has two halves, and two words for them. **The words are load-bearing, not decorative** —
they encode the studio's actual operating rhythm.

## Field

**One production's own open, explorable diorama space.**

- Replaces an earlier "room" idea. A Field is **walkable and pastoral, not boxed in** — closer to
  *Field of Dreams* than to a gallery room.
- Each production gets its own Field, reached from a central Dreamland hub.
- Built as **2D/2.5D layered parallax** — chibi-illustrated, efficient by construction. See
  [[efficient-motion]].
- Its own palette accent, its own character poses.
- **Not a portfolio grid.** The structural precedent is Cartier's six self-contained rooms, rescaled
  to a two-person studio and opened out into fields.

**Front-of-house.** Minimal chrome, mystique-forward. Process depth does not live here.

## Forest

**That production's living continuity layer.** It grows at the edge of its Field.

- A **sapling per monthly** consolidation.
- A fuller **grove per season**.
- Sourced automatically from real GitHub activity on that production's repo. No manual redesign,
  ever — the template is fixed, only the data changes.
- This is the "behind the scenes" destination, kept **separate** from the Field so the front stays
  calm while the Forest quietly thickens underneath.

The research found that separation is what good studio sites actually do: Active Theory's technical
write-ups live on a separate publication, basement.studio has a "Lab," Bruno Simon has a "Behind the
Scene" page. **Process content earns more trust living apart from the polished result.**

## Why the metaphor is literal

The monthly/seasonal clock is **not an arbitrary schedule.** The founders align it across:

- Natural seasons — four
- Agricultural cycles — planting, growing, harvest, rest
- Business quarters — four, mapping onto four seasons
- The website's Forest — sapling per month, grove per season
- [[../../productions/whimsy-fairy-journal/PROJECT|Whimsy]]'s seasonal recaps — the same clock, sold outward

*"It's all part of the rhythm of the studio on every level."*

So **Field, Forest, sapling, grove** are not chosen for charm. They describe how the studio actually
runs. Two consequences:

1. **Seasonal variation is a first-class token layer** in the design system — not a seasonal promo.
   See [[../../brand/DESIGN_SYSTEM|DESIGN_SYSTEM.md §1.8]].
2. **The Forest's clock is the business clock.** Exercising one exercises the other.

## The engine underneath

The Forest is one of **three** consumers of the same narrative engine — the studio's core technology.
See [[../../research/synthesis-cross-findings|synthesis §2]].

| Consumer | Reads | Produces |
|---|---|---|
| **Forest** (site) | GitHub activity | Seasonal story of the studio's work |
| **Whimsy** (product) | Journals, notes, doodles | Seasonal personalised storyline |
| **Couple App** (product) | Shared relationship data | Likely the same |

**Build the Forest first.** Real data, own repos, no users, no private data, no support burden — the
cheapest possible development environment for the studio's most valuable asset.

## Related

- [[efficient-motion]] · [[reduced-motion-first]] · [[asset-export-rules]]
- [[../../research/case-study-02-living-pipeline|CS02]] — the five-stage Forest architecture
