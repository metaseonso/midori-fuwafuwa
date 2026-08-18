---
title: "Couple App (name TBD)"
studio: Midori Fuwafuwa Studio
status: intake — concept stage, minimal detail
date_added: 2026-08-19
---

# Couple App (name TBD)

## What it is
A couple app. Described by the founders as *"very us (Midori Fuwa Fuwa)"* — meaning rooted
in Seonso and Grumpy Carrot's own relationship rather than built as a generic product for a
market.

No reference image yet. No name yet.

## Reading of "very us"
Taken as: the app is authentically theirs, grown from how the two of them actually operate as
a couple, and the studio's identity is inseparable from it. The studio is a partnership
between two people; a couple app is the most direct possible expression of that.

*(This is an interpretation of a short note — worth confirming.)*

## Likely shares the narrative engine

The studio now has three productions, and the same engine appears in at least two of them,
probably all three:

- **Studio Forest** (website) — real GitHub activity → seasonal story.
- **Whimsy** — personal journals, notes, doodles → seasonal personalised story.
- **Couple app** — shared relationship data (memories, milestones, plans, notes) → almost
  certainly the same treatment.

If that holds, the couple app is the third consumer of the one genuinely custom piece of
technology in the whole studio: narrative-arc construction plus story-relevant asset
curation. See `research/synthesis-cross-findings.md`.

**Practical consequence:** do not design this as a standalone app. Design it as a second
front-end onto the same engine Whimsy uses, with a different input schema and a different
skin. Two products sharing one engine is dramatically cheaper than two products.

## Privacy — same class as Whimsy, arguably higher
Shared relationship data is sensitive personal data, and a couple app may hold materially
more intimate content than a solo journal. Whatever data policy and architecture Whimsy
settles on — local synthesis, private cloud, or a zero-retention API arrangement — this
production inherits it, and should be considered when that decision is made rather than
after.

Additional wrinkle unique to this production: **two people share one account's data.** That
raises questions a solo journal never faces — consent when one partner exports or deletes,
what happens to shared history if the couple separates, and whether either partner can
unilaterally remove content the other contributed. Worth deciding deliberately rather than
inheriting whatever the database happens to do.

## Still needed
- The name.
- Platform: mobile app, web, both.
- What it actually does day to day — the concrete feature set.
- Whether it shares the Whimsy engine (see above), and if so how much of it.
- Reference art / visual direction.
- Whether it is a public product or a private tool for the two of them that may later ship.

## Intake log
- 2026-08-19: Production created from a brief note. Minimal detail captured; flagged as a
  likely third consumer of the shared narrative engine.
