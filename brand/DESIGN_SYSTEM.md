---
title: "Midori Fuwafuwa Studio — Design System"
date: 2026-08-19
status: v2 — derived from the studio reference image alone
source_of_truth: brand/logo/midori_fuwafuwa_logo_official.png
method: hex values sampled programmatically from the logo; contrast ratios computed, not estimated
---

# Midori Fuwafuwa Studio — Design System

## 0. The one reference

**There is one Midori Fuwafuwa reference image:**

```
brand/logo/midori_fuwafuwa_logo_official.png
```

The mint-green fluffy cloud mascot painting at a wooden easel, on cream. That image is the
entire design language of the production site. Every value in this document is sampled from it.

**Nothing else feeds this system.**

- The **artist personas** — Seonso and Grumpy Carrot — established the studio and work in it.
  **They each have their own distinct style, deliberately.** Their reference sheets are records
  of *their* styles, not of the studio's. Their palettes are documented separately in
  `brand/characters/PERSONA_PALETTES.md` and are **not** studio tokens.
- **Production reference images** (The Kits, Whimsy) are vision anchors for those productions —
  mood, world, composition. They are not studio style references either. Their palettes live
  with their productions.

If a colour, shape, or texture is not in the logo, it is not in this system. Additions are a
deliberate change to this document, not a borrowing from elsewhere.

---

## 1. Palette — sampled from the logo

Every value below was read out of the logo file with PIL. Nothing is eyeballed.

### 1.1 Ground

| Token | Hex | Where it comes from |
|---|---|---|
| `--ground` | `#F4EDD8` | The cream parchment field — roughly half the logo |
| `--ground-warm` | `#F7EDD8` | Warmer cream variant |
| `--surface` | `#FFFFFF` | Raised panels |

### 1.2 Mint — the mascot

| Token | Hex | Where it comes from |
|---|---|---|
| `--mint` | `#BEECCE` | Cloud body, most saturated point |
| `--mint-soft` | `#D1EFDE` | Cloud mid-tone |
| `--mint-highlight` | `#EDF1EB` | Cloud highlight |
| `--mint-deep` | `#556A5C` | **Derived** from `--mint` for text use — see 1.6 |

### 1.3 Blush

| Token | Hex | Where it comes from |
|---|---|---|
| `--blush` | `#F8D1D1` | Mascot cheek |
| `--blush-pale` | `#FCF2F4` | Pink wash at the cloud's crown |

### 1.4 Ink and sage

| Token | Hex | Where it comes from |
|---|---|---|
| `--ink` | `#492C12` | "STUDIO" lettering, darkest point in the logo |
| `--ink-green` | `#424B3A` | Mascot's eyes, darkest point |
| `--sage` | `#748872` | Arc lettering mid-tone |
| `--sage-pale` | `#DADBCE` | Pale sage field |

### 1.5 Wood

| Token | Hex | Where it comes from |
|---|---|---|
| `--wood` | `#825E46` | The easel |
| `--wood-deep` | `#784E35` | Easel shadow |
| `--tan` | `#D0B195` | Ground shadow beneath the mascot |

That is the whole palette: **fifteen values, one image.** It is deliberately small. A cream
ground, a mint, a blush, two inks, two sages, three woods. Everything the site needs.

### 1.6 Contrast — computed, with failures named

| Foreground | Background | Ratio | Verdict |
|---|---|---|---|
| `--ink` `#492C12` | `--ground` | **10.86** | AAA |
| `--ink-green` `#424B3A` | `--ground` | **7.81** | AAA |
| `--mint-deep` `#556A5C` | `--ground` | **4.98** | AA |
| `--wood` `#825E46` | `--ground` | **4.93** | AA |
| `--sage` `#748872` | `--ground` | 3.26 | **AA — large text only** (24px+, or 19px+ bold) |
| `--mint` `#BEECCE` | `--ground` | 1.12 | **FAILS — decoration only** |

**Hard rules:**
- Default body text is `--ink` on `--ground`.
- `--mint` is **never text on a light ground.** It is fill, stroke, glow, wash. For minty text,
  use `--mint-deep`.
- `--sage` is for large text and UI strokes only.

### 1.7 Dark mode

| Token | Hex |
|---|---|
| `--ground-dark` | `#231F1C` |
| `--surface-dark` | `#2A2622` |

A warm near-black, not a neutral grey — the logo's whole character is warm, and a cold grey
breaks it.

On `--ground-dark`: `--ground` as text reads 13.98:1 (AAA), and `--mint` reads 12.52:1 (AAA).
**Mint becomes text-safe in dark mode**, which it is not in light mode.

### 1.8 Seasonal layer

The studio runs one clock across natural seasons, agricultural cycles, business quarters, the
website's Forest, and Whimsy's recaps. This system expresses that by overriding **two tokens
per season, and nothing else.**

| Season | Agricultural phase | `--season-accent` | `--season-ground` |
|---|---|---|---|
| Spring | Planting | `#BEECCE` — `--mint` | `#F7F2E4` |
| Summer | Growing | `#748872` — `--sage` | `#F4EDD8` |
| Autumn | Harvest | `#D0B195` — `--tan` | `#F5E9D2` |
| Winter | Rest | `#DADBCE` — `--sage-pale` | `#F2EFE6` |

Note that all four accents are already logo colours. **The seasons are the logo's own palette,
rotated** — no new hues enter the system. A season should feel like the same world in a
different month, not a redesign.

---

## 2. Typography

All faces are **SIL Open Font License**. Hard requirement: OFL permits commercial use and
bundling, and the studio may put work on merchandise. "Free for personal use" faces are
disqualified outright.

| Role | Face | Licence | Why |
|---|---|---|---|
| Display / headings | **Baloo 2** | OFL 1.1 | Rounded, chunky, warm — the closest real match to the logo's hand-lettering weight |
| Body / UI | **Nunito** | OFL 1.1 | Rounded terminals echo the brand quietly. Excellent small-size legibility, wide weight range |
| Hangul | **Gowun Dodum** | OFL 1.1 | Clean Korean face for 선소 and any Hangul on the site. Pairs with Nunito's weight |
| Handwritten accent | **Caveat** | OFL 1.1 | Accent only, never body copy |

### Scale — 1.25 ratio, 16px root

| Token | Size | Line height | Use |
|---|---|---|---|
| `--text-xs` | 12px | 1.5 | Captions, metadata |
| `--text-sm` | 14px | 1.55 | Secondary text |
| `--text-base` | 16px | 1.6 | Body |
| `--text-lg` | 20px | 1.5 | Lead paragraphs |
| `--text-xl` | 24px | 1.35 | Sub-headings |
| `--text-2xl` | 31px | 1.25 | Section headings |
| `--text-3xl` | 39px | 1.15 | Field titles |
| `--text-4xl` | 49px | 1.1 | Hero |

Never below 14px for running text.

**Loading:** WOFF2 only, subset aggressively. `font-display: swap` for Baloo 2 (the brand voice
matters). `font-display: optional` for Caveat (an accent face is not worth a layout shift).

---

## 3. Spacing, radius, elevation

**Spacing — 4px base:** 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128

**Radius — the logo has no sharp corner anywhere, and neither does this system:**

| Token | Value | Use |
|---|---|---|
| `--radius-sm` | 8px | Tags, chips |
| `--radius-md` | 16px | Buttons, inputs |
| `--radius-lg` | 24px | Cards, panels |
| `--radius-xl` | 32px | Field cards, large surfaces |
| `--radius-full` | 9999px | Pills, mascot frames |

A 0px radius is off-brand.

**Elevation — warm-tinted, never black.** Black shadows read cold against cream.

| Token | Value |
|---|---|
| `--shadow-sm` | `0 1px 3px rgba(73, 44, 18, 0.08)` |
| `--shadow-md` | `0 4px 12px rgba(73, 44, 18, 0.10)` |
| `--shadow-lg` | `0 12px 32px rgba(73, 44, 18, 0.12)` |
| `--shadow-glow` | `0 0 24px rgba(190, 236, 206, 0.45)` — the one "magic" shadow, mint |

---

## 4. Motion

### Three rules, no exceptions

1. **Animate `transform` and `opacity` only.** Anything touching layout forces reflow on the
   main thread.
2. **Native CSS scroll-driven animation is primary** — `animation-timeline: scroll()` / `view()`
   with `animation-range`. Compositor-only, no scroll listener. Guard with
   `@supports (animation-timeline: scroll())` and fall back to a **static state**, not a JS
   polyfill — a polyfill cancels out the entire performance win.
3. **GSAP + Lenis is the secondary layer only**, for choreography CSS timelines cannot express:
   pinned sections, scrubbed sequences, staggered batches. Use `ScrollTrigger.batch()`, not
   per-element triggers. Read DOM values, then write them — never interleaved.

### Durations and easing

| Token | Value | Use |
|---|---|---|
| `--dur-micro` | 120ms | Hover, focus, press |
| `--dur-ui` | 200ms | Buttons, toggles, tooltips |
| `--dur-enter` | 320ms | Element reveals |
| `--dur-scene` | 600ms | Field transitions |
| `--dur-ambient` | 2400ms | Ambient drift — cloud bob, sparkle |

| Token | Curve | Use |
|---|---|---|
| `--ease-standard` | `cubic-bezier(0.4, 0, 0.2, 1)` | Default |
| `--ease-out-soft` | `cubic-bezier(0.16, 1, 0.3, 1)` | Entrances |
| `--ease-bounce` | `cubic-bezier(0.34, 1.36, 0.64, 1)` | **Mascot only.** The overshoot is personality; on UI it reads unserious |

### Reduced motion is the baseline

Design the static state first. It is the primary design, not a fallback — rich motion layers on
top for those who have not asked for less.

Under `prefers-reduced-motion: reduce`:
- Parallax layers hold at resting offsets. The result is a still, softly-lit diorama — already a
  finished, beautiful outcome, and the fastest possible page.
- Ambient loops stop entirely.
- Any WebGL accent **never initialises** — skip the download, the GPU cost, the scene graph. Do
  not merely pause it.
- Opacity cross-fades up to `--dur-ui` may remain; they convey state, not motion.

---

## 5. Components

A small set. Resist adding more.

**Field card (hub entry)** — the gateway into one production's Field. `--radius-xl`,
`--shadow-md`, `--ground`. Title in Baloo 2 at `--text-2xl`, one line of description, a mascot
slot. Hover lifts `translateY(-4px)` over `--dur-ui`. **No scale** — scaling illustration
reveals raster softness.

**Scene block (Forest recap)** — one beat of a generated story. Data-driven: iterates the
manifest's `scenes[]` array, so a new month never touches code. Holds one real committed asset,
prose, a mood tag, and a source link back to the originating PR or issue. Reveals via
`animation-timeline: view()`.

**Mascot slot** — a reserved, fixed-aspect region. The only place `--ease-bounce` and ambient
loops are permitted, because this is what carries personality. Fixed aspect ratio prevents
layout shift as art loads.

**Navigation** — minimal chrome. Mystique carries the front page. Text links in `--ink`,
`--radius-full` on any pill treatment, no dropdown trees.

**Text surface** — a readable panel over illustrated ground. `--ground` at 92% opacity minimum
behind body copy. Illustration must never push text contrast below the ratios in 1.6.

---

## 6. Illustration and asset rules

**The logo is the model.** Soft, rounded, flat-with-gentle-shading, warm. Match it.

**Line.** Soft, slightly variable weight. Never a hard technical stroke. Outline colour is a
darkened version of the fill — never pure black. `--ink` is the darkest line permitted.

**Palette discipline.** Every studio-level asset draws from section 1 and nowhere else. If a
piece seems to need a new hue, that is a deliberate change to this document.

**Layering for parallax.** Author Field art as separate transparent layers: sky/far, mid,
subject, near, foreground. Five layers or fewer per Field — past that, compositing stops being
free.

**Export.**
- Flat-colour vector → **optimised SVG.** Run SVGO, strip editor metadata.
- Flat-colour raster with hard edges → **PNG-8** or lossless WebP. Usually smaller than lossy
  formats for this style.
- Textured/painterly pieces → **AVIF with WebP fallback.** These behave photographically.
- Never ship a raw PNG-24 of a flat illustration — several times larger for no visible gain.
- `loading="lazy"` below the fold. Native, no library.
- Explicit `width`/`height` or `aspect-ratio` on every image. No layout shift.

---

## 7. Tokens as code

```css
:root {
  /* ---- ground ---- */
  --ground: #F4EDD8;
  --ground-warm: #F7EDD8;
  --surface: #FFFFFF;

  /* ---- mint (mascot) ---- */
  --mint: #BEECCE;           /* decoration only on light */
  --mint-soft: #D1EFDE;
  --mint-highlight: #EDF1EB;
  --mint-deep: #556A5C;      /* text-safe — 4.98:1 */

  /* ---- blush ---- */
  --blush: #F8D1D1;
  --blush-pale: #FCF2F4;

  /* ---- ink & sage ---- */
  --ink: #492C12;            /* default body text — 10.86:1 */
  --ink-green: #424B3A;      /* 7.81:1 */
  --sage: #748872;           /* large text / strokes only — 3.26:1 */
  --sage-pale: #DADBCE;

  /* ---- wood ---- */
  --wood: #825E46;           /* 4.93:1 */
  --wood-deep: #784E35;
  --tan: #D0B195;

  /* ---- semantic roles ---- */
  --text-primary: var(--ink);
  --text-emphasis: var(--ink-green);
  --text-muted: var(--wood);
  --accent: var(--mint);
  --accent-text: var(--mint-deep);

  /* ---- seasonal (default: summer) ---- */
  --season-accent: #748872;
  --season-ground: #F4EDD8;

  /* ---- type ---- */
  --font-display: "Baloo 2", system-ui, sans-serif;
  --font-body: "Nunito", system-ui, sans-serif;
  --font-hangul: "Gowun Dodum", var(--font-body);
  --font-hand: "Caveat", cursive;

  --text-xs: 0.75rem;   --lh-xs: 1.5;
  --text-sm: 0.875rem;  --lh-sm: 1.55;
  --text-base: 1rem;    --lh-base: 1.6;
  --text-lg: 1.25rem;   --lh-lg: 1.5;
  --text-xl: 1.5rem;    --lh-xl: 1.35;
  --text-2xl: 1.953rem; --lh-2xl: 1.25;
  --text-3xl: 2.441rem; --lh-3xl: 1.15;
  --text-4xl: 3.052rem; --lh-4xl: 1.1;

  /* ---- space ---- */
  --space-1: 4px;   --space-2: 8px;   --space-3: 12px;  --space-4: 16px;
  --space-6: 24px;  --space-8: 32px;  --space-12: 48px; --space-16: 64px;
  --space-24: 96px; --space-32: 128px;

  /* ---- radius ---- */
  --radius-sm: 8px;  --radius-md: 16px; --radius-lg: 24px;
  --radius-xl: 32px; --radius-full: 9999px;

  /* ---- elevation ---- */
  --shadow-sm: 0 1px 3px rgba(73, 44, 18, 0.08);
  --shadow-md: 0 4px 12px rgba(73, 44, 18, 0.10);
  --shadow-lg: 0 12px 32px rgba(73, 44, 18, 0.12);
  --shadow-glow: 0 0 24px rgba(190, 236, 206, 0.45);

  /* ---- motion ---- */
  --dur-micro: 120ms;  --dur-ui: 200ms;    --dur-enter: 320ms;
  --dur-scene: 600ms;  --dur-ambient: 2400ms;
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-out-soft: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-bounce: cubic-bezier(0.34, 1.36, 0.64, 1);
}

/* ---- seasonal layer: two tokens, all four drawn from the logo ---- */
[data-season="spring"] { --season-accent: #BEECCE; --season-ground: #F7F2E4; }
[data-season="summer"] { --season-accent: #748872; --season-ground: #F4EDD8; }
[data-season="autumn"] { --season-accent: #D0B195; --season-ground: #F5E9D2; }
[data-season="winter"] { --season-accent: #DADBCE; --season-ground: #F2EFE6; }

/* ---- dark mode ---- */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ground: #231F1C;
    --surface: #2A2622;
    --text-primary: #F4EDD8;
    --text-emphasis: #FFFFFF;
    --text-muted: #DADBCE;
    --accent-text: var(--mint);   /* mint IS text-safe on dark — 12.52:1 */
  }
}
:root[data-theme="dark"] {
  --ground: #231F1C;
  --surface: #2A2622;
  --text-primary: #F4EDD8;
  --text-emphasis: #FFFFFF;
  --text-muted: #DADBCE;
  --accent-text: var(--mint);
}

/* ---- reduced motion: the baseline, not a fallback ---- */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Note on what is deliberately absent:** there is no persona layer and no production layer in
this token block. The personas have their own styles; productions have their own vision. Neither
overrides the studio's system. If a Field needs to feel like its production, it does so through
art inside the Field — not by re-tinting the studio's tokens.

---

## 8. Open questions

1. **The logo's arc lettering has no clean sample.** It carries a white outline over a
   mint-to-pink gradient, so every pixel sample blends. Baloo 2 is the closest real face; if
   the studio wants that exact lettering as a wordmark, redraw it as vector art rather than
   setting it in type.
2. **Hangul and Latin pairing is untested.** Gowun Dodum is recommended on licence and
   character, but compare it optically against Nunito at real sizes before locking.
3. **The five-layer parallax budget is a starting rule, not a measured limit.** Verify on a
   mid-range phone once the first Field exists.
4. **Dark mode may not be wanted at all.** The logo is emphatically a light, cream-ground
   design. Dark tokens are provided because the viewer's system may demand them, but a
   deliberate light-only commitment is a legitimate choice for this brand.
