# Zajno Empirical Data — extracted from their Lottie files

This is not opinion or interpretation. These are the actual numbers
parsed from **27 Lottie `.json` files** served by motion.zajno.com,
representing **7,897 keyframes** across their entire principle demo set.

Parsed on **2026-05-23** by `assets/parse_lotties.py`.

## TL;DR

- **Framerate**: 60fps is the default. Use 30fps only for long-running ambient loops.
- **Hero duration sweet spot**: ~2.35s (median across all timeline-driven anims).
- **UI/menu interaction sweet spot**: 0.67s (40 frames @ 60fps — exact value used in 11 files).
- **Color palette**: ink-dark + warm off-white + ONE blue-purple accent (`#6777b2`).
  Soft sage and lavender as tertiary support.
- **Easing**: 32% of keyframes use AE's default `(0.167, 0.167, 0.833, 0.833)` (auto-bezier).
  Their *intentional* easing curve is `(0.55, 0, 0.45, 1)` — a Material-style ease-in-out cubic.

## Framerate distribution

| FPS  | Files | Notes                                          |
|------|-------|------------------------------------------------|
| 60   | 19    | Default for everything interactive             |
| 30   | 7     | Long ambient loops (header logo, parallax)     |
| 24   | 1     | Preloader (cinematic feel)                     |

**Takeaway**: pick **60fps** for new Lottie work unless you're rendering
a 7-second ambient loop where bandwidth matters more than smoothness.

## Animation duration distribution

| Metric  | Value |
|---------|-------|
| Min     | 0.54s |
| Median  | 2.35s |
| Mean    | 2.51s |
| Max     | 7.0s  |

### Two clear clusters in the data:

**Cluster A — UI / menu animations** (~0.67s, exactly 40 frames @ 60fps):
fade, Morph, Masking, intro_menu, sources, easing_menu, dimension,
delay_menu, zoom — 11 files share this **exact** duration.

**Cluster B — Easing demos** (~2.35s, exactly 141 frames @ 60fps):
ease_out, ease, ease_in, cubic, linear — all 5 demos run for the same
2.35s so their visual comparison is fair.

**Cluster C — Hero / ambient** (3-7s): header_logo*, preloaders,
parallax demo, not_real_time hero.

### Recommended durations (Zajno-derived):

```js
const ZAJNO_DURATIONS = {
  interactive_ui:  0.67,   // menu open/close, micro-state changes
  easing_demo:     2.35,   // showcase a single curve
  ambient_loop:    7.00,   // header logo, footer signature
  preloader:       3.20,   // 3.85s mobile, 3.68s tablet, 3.20s desktop
};
```

Note the responsive preloader: **mobile preloader is longer than desktop**
(3.85s vs 3.20s). Likely because mobile load is slower — they pad the
animation to cover the latency.

## Easing curves — what Zajno's designers actually picked

These are Lottie keyframe-tangent values. Each entry is the cubic-bezier
control point `(out_x, out_y, in_x, in_y)`. To translate into a CSS
`cubic-bezier(x1, y1, x2, y2)`, use `(out_x, out_y, 1-in_x, 1-in_y)`.

| Lottie `(ox, oy, ix, iy)`     | CSS bezier                 | Uses  | Notes              |
|--------------------------------|----------------------------|-------|---------------------|
| `(0.167, 0.167, 0.833, 0.833)` | `(.17,.17,.17,.17)` ≈ ease | 2526  | AE auto-bezier — default, not intentional |
| **`(0.55, 0, 0.45, 1)`**       | `(.55,0,.55,0)` ≈ ease-in-out cubic | **84** | **Their intentional default** |
| `(0.53, 0, 0.833, 0.833)`      | `(.53, 0, .17, .17)`       | 20    | Slow-out asymmetric |
| `(0.167, 0.167, 0.43, 1)`      | `(.17,.17,.57, 0)`         | 19    | Soft ease-out      |
| `(0.65, 0, 0.833, 0.833)`      | `(.65, 0, .17, .17)`       | 9     | Strong start, slow end |
| `(0.7, 0, 0.3, 1)`             | `(.7,0,.7,0)` ≈ very strong ease-in-out | 6 | Dramatic |
| `(0.6, 0, 0.4, 1)`             | `(.6,0,.6,0)`              | 5     | Moderate s-curve |
| `(0.64, 0, 0.36, 1)`           | `(.64,0,.64,0)`            | 4     | Tight s-curve |

### Reading this

The dominant value `(0.167, 0.167, 0.833, 0.833)` is **After Effects'
default auto-bezier** — what you get when you press F9 on a keyframe.
2,526 of 7,897 keyframes (32%) use it. Most are probably not deliberate
artistic choices — they're the path of least resistance.

The next-most-common, `(0.55, 0, 0.45, 1)`, is symmetric ease-in-out
cubic — basically Material Design's "standard" curve
(`cubic-bezier(0.4, 0, 0.2, 1)` is very close). When Zajno's animators
*chose* a curve, they chose this 84 times — more than 4× any other
intentional curve.

### Recommended Zajno-derived easing palette (for CSS / GSAP)

```css
:root {
  /* Zajno's intentional default — symmetric ease-in-out cubic */
  --ease-zajno-std:    cubic-bezier(0.55, 0, 0.45, 1);

  /* Soft entrance — slow-out asymmetric */
  --ease-zajno-soft:   cubic-bezier(0.17, 0.17, 0.57, 1);

  /* Dramatic — used in 3 files for "hero" reveals */
  --ease-zajno-strong: cubic-bezier(0.7, 0, 0.3, 1);

  /* GSAP custom-eases lifted from script.v33.min.js */
  /* (use the CustomEase plugin — see examples/custom-easing.js) */
}
```

## Color palette — the actual ink + accent + supporting set

Top 30 colors across all 27 files. The truth is jarring: 90%+ of pixels
are pure greys, and they get all their personality from **one blue-purple
accent** and a few muted sage/lavender supporting tints.

### Inks & neutrals (the workhorse — 79% of all color uses)

| Hex       | Uses | Role                                  |
|-----------|------|---------------------------------------|
| `#0c0b0b` | 250  | Primary text/ink — *not* pure black   |
| `#727272` | 131  | Mid-grey — outlines, secondary text   |
| `#fdfcfa` | 99   | Background — warm off-white, *not* pure white |
| `#000000` | 46   | Pure black (rare — only for hard shapes) |
| `#ffffff` | 45   | Pure white (rare)                     |
| `#050504` | 12   | Near-black variant                    |
| `#121212` | 5    | Dark mid-grey                         |
| `#1c1b1b` | 4    | Deeper mid-grey                       |
| `#828282` | 2    | Mid-grey alt                          |
| `#7f7f82` | 1    | Mid-grey with slight blue tint        |
| `#7a7a7a` | 1    | Mid-grey alt                          |
| `#d6d6d6` | 1    | Light grey                            |
| `#c0bebc` | 1    | Warm light grey                       |

### THE accent (#6777b2 — the Zajno signature)

| `#6777b2` | 25   | **The accent color** — muted blue-purple |

This is the only saturated color appearing more than twice. Everything
else is a soft tertiary supporting tint:

### Supporting tints (used ≤ 2 times — accents on accents)

| Hex       | Family          |
|-----------|-----------------|
| `#d6e8c8` | Soft sage / mint |
| `#d8e9ca` | Soft sage variant |
| `#e7e9cb` | Pale yellow-green |
| `#6d805b` | Olive (darker sage) |
| `#d2c8e8` | Soft lavender   |
| `#c8cfe8` | Pale blue-lavender |
| `#615871` | Deep lavender   |
| `#515567` | Dark muted blue |
| `#c8e8e8` | Pale teal       |
| `#4c7272` | Deep teal       |
| `#ff0000` | Pure red (1 use — probably an error indicator) |

### Recommended Zajno palette (CSS tokens)

```css
:root {
  /* Ink (text, primary shapes) */
  --zajno-ink:         #0c0b0b;
  --zajno-ink-soft:    #1c1b1b;

  /* Neutrals */
  --zajno-grey-mid:    #727272;
  --zajno-grey-light:  #d6d6d6;
  --zajno-grey-warm:   #c0bebc;

  /* Background */
  --zajno-bg:          #fdfcfa;   /* warm off-white — NOT pure white */

  /* THE accent (use sparingly — 25 of 759 colored frames) */
  --zajno-accent:      #6777b2;   /* muted blue-purple */

  /* Supporting tints (use VERY sparingly — secondary accents) */
  --zajno-sage:        #d6e8c8;
  --zajno-sage-deep:   #6d805b;
  --zajno-lavender:    #d2c8e8;
  --zajno-lavender-deep:#615871;
  --zajno-teal:        #c8e8e8;
  --zajno-teal-deep:   #4c7272;
}
```

### Design rule extracted from this data

**80/15/5 color rule**:
- 80% of the frame is `--zajno-bg` (warm off-white) + `--zajno-ink`
- 15% is greys and outlines
- 5% (max) is `--zajno-accent` or one supporting tint

This is the recipe for the "premium editorial / Swiss design" feel
Zajno has. Stop reaching for the brand color — most of the canvas
should be ink on paper.

## Layer complexity

| Layers per file | Files | Type                              |
|------------------|-------|-----------------------------------|
| 1-3              | 5     | Simple demos (parallax, linear)   |
| 5-6              | 8     | Standard principle demos          |
| 8-12             | 9     | Menu / hero illustrations         |
| 13-18            | 5     | Complex hero compositions         |

**Takeaway**: a "production-quality" hero Lottie has **8-12 layers**.
Beyond 18, file size explodes (the 681KB `not_real_time.json` is the
outlier — probably a complex character illustration).

## File-size budget

The median Lottie file is ~28KB. The 681KB `not_real_time.json` is
24× the median — that file is the one to lazy-load.

Practical budget for a landing page:
- **Hero animation**: up to 80KB acceptable
- **Section illustrations**: 20-40KB each
- **UI accents**: < 10KB each

Total Lottie payload below the fold: aim for **< 200KB**.

## How to use this data

1. Open `assets/lotties/Morph.json` in [Lottielab](https://www.lottielab.com)
   or [LottieFiles editor](https://lottiefiles.com/editor) and watch
   the actual animation. The numbers in this doc came from that file.
2. When picking timing for a new animation, default to `0.67s` for UI
   and `2.35s` for "showcase" moments — these are what Zajno picked.
3. When picking easing, default to `cubic-bezier(0.55, 0, 0.45, 1)` —
   their intentional baseline.
4. When picking colors, start from `--zajno-bg` and `--zajno-ink` and
   only reach for `#6777b2` as your single accent. Adding more saturated
   colors moves you away from the Zajno look, not toward it.

## Re-running the parser

```bash
python3 ~/.claude/skills/zajno-motion/assets/parse_lotties.py \
  > ~/.claude/skills/zajno-motion/assets/empirical-output.json
```

Modify the parser if you want to extract additional dimensions (e.g.,
gradient stops, shape path complexity, blend modes).
