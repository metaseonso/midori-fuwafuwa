---
title: Reduced motion first
tags: [craft, accessibility, performance, principle]
status: settled — a founding principle, not a fallback
updated: 2026-08-19
source: research/case-study-01-immersive-efficiency.md
---

# Reduced motion first

**Design the static state first. It is the primary design, not a fallback.** Rich motion layers on
top, for people who have not asked for less.

## Why this is not a compromise here

For this brand it is genuinely not a sacrifice:

> A static, softly-lit diorama of a [[field-and-forest|Field]], mascots in their resting poses, is
> **already a beautiful outcome.**

It is also **the fastest possible page.** Which means the most accessible path and the cheapest path
are the same code path. That is unusual and worth exploiting rather than treating as a constraint.

## What `prefers-reduced-motion: reduce` must do

Not just "animate less" — **gate whether expensive things initialise at all.**

| Layer | Behaviour under reduced motion |
|---|---|
| Parallax layers | Hold at resting offsets. Still diorama. |
| Ambient loops — cloud bob, sparkle drift | Stop entirely |
| WebGL accent | **Never initialises.** Skip the asset download, the GPU cost, the scene graph. Do not merely pause it. |
| Scroll-linked reveals | Static, or a short opacity fade |
| Opacity cross-fades ≤ 200ms | May remain — they convey *state*, not motion |

The WebGL row is the important one. Pausing a canvas still paid for downloading and building it.
Gating initialisation skips the whole cost.

## A quiet bonus

WCAG places motion criteria at the stricter **AAA** level. Designing reduced-motion-first means the
site **exceeds the typical AA litigation baseline on motion specifically** — a genuine head start,
though not sufficient on its own for full-site AA conformance.

## Still to specify

Reduced motion is settled. The rest of accessibility is not yet written down: keyboard navigation,
visible focus states, alt-text discipline, heading order, and colour-independent meaning. The
[[../../brand/DESIGN_SYSTEM|design system]] covers contrast; the rest is an open item.

## Related

- [[efficient-motion]] — the layer this sits under
- [[../../brand/DESIGN_SYSTEM|DESIGN_SYSTEM.md §4]] — the reduced-motion CSS block
