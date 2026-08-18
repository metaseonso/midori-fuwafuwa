---
title: Asset export rules
tags: [craft, performance, assets, production]
status: settled
updated: 2026-08-19
---

# Asset export rules

**Half the performance battle is won before any animation code runs.** Format choice should follow
the art style, not a blanket rule.

## Format by art type

| Art type | Format | Why |
|---|---|---|
| Flat-colour **vector** | **Optimised SVG** | Run SVGO, strip editor metadata. Scales free. |
| Flat-colour **raster**, hard edges | **PNG-8** or lossless WebP | Often *smaller* than lossy formats for flat art |
| **Painterly / watercolour** textures | **AVIF** with WebP fallback | These behave photographically |
| Photographs | AVIF / WebP | Standard |

⚠️ **Never ship a raw PNG-24 of a flat illustration.** It is typically several times larger for no
visible gain. This is the most common single waste in illustrated sites.

## Parallax layering

Author [[field-and-forest|Field]] art as separate transparent layers:

```
sky / far  →  mid  →  subject  →  near  →  foreground
```

Each gets its own scroll speed. **Five layers or fewer per Field** — past that, compositing stops
being free.

*(That budget is a starting rule, not a measured limit. Verify on a mid-range phone once the first
Field exists.)*

## Loading discipline

- `loading="lazy"` on everything below the fold. Native, no library needed.
- **Explicit `width`/`height` or `aspect-ratio` on every image.** No layout shift, ever.
- Fonts: **WOFF2 only**, subset aggressively.
- `font-display: swap` where the brand face matters; `optional` where a layout shift would hurt more
  than a substitution.
- **Self-host everything** — fonts, scripts, styles. Third-party requests are both a performance cost
  and a privacy problem. See [[../site/cookie-traps]].

## Palette discipline

Every studio-level asset draws from the [[../../brand/DESIGN_SYSTEM|design system]] palette and
nowhere else. If a piece seems to need a new hue, that is a deliberate change to the design system —
not a one-off.

## Related

- [[efficient-motion]] — what happens after assets load
- [[../site/cookie-traps]] — why self-hosting matters twice
- [[../../brand/DESIGN_SYSTEM|DESIGN_SYSTEM.md §6]] — illustration rules
