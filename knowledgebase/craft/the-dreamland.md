---
title: The Dreamland — the site concept
tags: [craft, site, concept, core]
status: direction set 2026-08-19 — details open
updated: 2026-08-19
---

# The Dreamland — the site concept

**ふわふわ / fuwa fuwa — soft, floaty, weightless, drifting.**

The studio is named for a feeling, and the site should *be* that feeling rather than depict a place
where work happens.

> **Founder, 2026-08-19: "I like the fuwa fuwa feel more than the studio feel."**

## What was rejected, and why it matters

An earlier concept — **The Easel** — made the logo literal: a studio interior, the mascot at its
easel, canvases leaning around the room, each canvas a dream field.

It was clever and it scaled. But it was **brand-literal rather than brand-true.** A studio is
furniture, architecture, a workplace. It has hard edges and a floor. That is the opposite of fuwa
fuwa.

**Retired as the site's framing.** The logo still shows the mascot at its easel — that is the
studio's *mark*, and it stays. The mark and the world do not have to be the same thing.

## The feeling, concretely

Fuwa fuwa means the site should have:

- **No hard architecture.** No rooms, no walls, no floor, no furniture. Nothing you could measure.
- **Soft edges everywhere.** Things fade rather than end. The design system already forbids a 0px
  radius; extend that instinct to the whole composition.
- **Weightlessness.** Elements drift rather than sit. Movement is buoyant, never mechanical.
- **Depth without structure.** You sense distance through layers and haze, not through perspective
  lines.
- **Quiet.** Minimal chrome, mystique-forward — which the research independently recommended.

**The mascot is already the thesis.** It is a small mint cloud. Fuwa fuwa is literally what a cloud
*is*. The site should feel like the inside of that character rather than the room it works in.

## The shape this suggests

A soft cloudscape you drift through, with the dream fields glimpsed below and entered by drifting
down into one.

Why this fits, beyond the feeling:

- **Clouds at different depths are the most natural parallax that exists.** The technique and the
  subject are the same thing, so the motion never looks applied.
- **Layered soft shapes are the cheapest possible art to produce and render** — which is the studio's
  own stated value principle, satisfied without compromise.
- **It scales.** A new production is another field below. Nothing restructures.
- **The still frame is finished.** Under [[reduced-motion-first]], a quiet layered cloudscape with
  the mascot drifting in it is already a complete, beautiful image.
- **Dreamland is the studio's actual premise.** Seonso and Grumpy Carrot share a Dreamland. The site
  is that place, not a depiction of it.

⚠️ **This is a direction, not a locked design.** The cloudscape is the most obvious expression of
fuwa fuwa and the one that best fits the parallax mechanics — but it is one interpretation. Worth
sketching before committing.

## The navigation model — confirmed, unchanged

> **"Scroll through the dream world, explore a field, see the forest within."**
> — the founders, 2026-08-19

| Level | Verb | What it is | Feeling |
|---|---|---|---|
| **1. The dream world** | **Scroll** | The hub. Drifting through the Dreamland; fields appear as you move | Drifting. No decisions required |
| **2. A dream field** | **Click** | One production's own explorable space. A chosen threshold | Arriving. A decision, not a corridor |
| **3. The forest within** | Scroll deeper | That production's living history, **inside** its field | Going deeper. A reward for curiosity |

**Scroll is for wandering. Click is for choosing.** Wandering should never require a decision;
choosing should never happen by accident.

This model survives the change of concept intact — it describes *movement*, not *scenery*.

## The Forest moved inside

Earlier research put the Forest *at the edge of* its Field. The founders' phrasing — **"see the
forest within"** — puts it inside, which is better:

- **Depth is the reward for interest.** Someone curious about how a production is made travels
  further in, rather than stepping sideways to a separate page.
- **The front of each field stays calm**, which is exactly the separation the research asked for.
- **The metaphor holds.** A forest inside a field is somewhere you walk into. A forest beside a field
  is scenery.

See [[field-and-forest]].

## Structure

```
/                     the dream world — drift, scroll
/fields/the-kits      a dream field — entered by click
/fields/whimsy
/fields/<production>
  └── the forest      within each field, reached by going deeper
/ethos                the studio's own words
/privacy  /terms      one screen each
```

Plus per-channel landing pages — see [[../site/measuring-arrival]].

⚠️ **Internal labels only.** "Dream field" and "forest" are structural vocabulary. What a visitor
sees labelled on screen is a separate creative decision, still open.

## Build constraints that apply immediately

⚠️ A drifting full-viewport cloudscape walks straight into two documented traps. Read
[[crawlers-and-parallax]] **before** building the hub:

- **Cap every `100vh` element with `max-height`.** Googlebot expands its viewport to full page
  height; an uncapped fullscreen hero can balloon to thousands of pixels and starve everything
  below it.
- **Content must exist in the HTML.** Googlebot does not scroll and no AI crawler runs JavaScript.
  Drift animations may only *animate* things that are already there.

## Still open

- **Is it clouds?** The most natural reading of fuwa fuwa, but worth sketching alternatives before
  locking.
- **Where do the fields sit** — below, through gaps, further along? This decides whether drifting is
  vertical, horizontal, or into depth.
- **How does entering a field feel?** Sinking into it is the obvious move. Must be `transform` and
  `opacity` only.
- **Does the mascot accompany you?** A companion drifting alongside is tempting, and must survive
  [[reduced-motion-first]] and the motion budget in [[efficient-motion]].
- **What the visitor actually sees labelled.** Internal vocabulary is settled; external copy is not.
- **Where the personas appear.** The studio level belongs to Seonso and Grumpy Carrot; each field
  belongs to its production's characters. The handover needs designing.

## Related

- [[field-and-forest]] · [[crawlers-and-parallax]] · [[efficient-motion]] · [[reduced-motion-first]]
- [[../../brand/DESIGN_SYSTEM|DESIGN_SYSTEM.md]] — the tokens this is built from
