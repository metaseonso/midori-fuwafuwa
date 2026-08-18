# Case Study — Luke Davis Instagram Reels

**Creator**: [@lukedavis.ig](https://www.instagram.com/lukedavis.ig/) — macro/crypto finance creator.

**Analyzed**: 2026-05-24, two posts (1.9k and 40.4k likes). Downloaded via yt-dlp,
analyzed with ffmpeg (scene detection, loudness profile, frame extraction).

## The format in one line

54-second, 1080×1920, zero-cut, animated-data-visualization Reels with continuous
voiceover and a DM-funnel CTA at the end.

## What this case study proves

The Zajno Motion Design System (color restraint, single accent, animation-as-motion-
not-decoration) **transfers directly** from editorial web design to short-form
social video. Luke Davis isn't using Zajno tokens explicitly, but he's applying the
same principles:

- One accent per video (orange in one, green in another) — Principle 1 (Easing) + 80/15/5
- Word-by-word text reveals — Principle 2 (Offset & Delay)
- Lines drawn in via Trim Path — Principle 3 (Fade combined with motion, not alone)
- Continuous composition, no cuts — animation IS the editing
- Restrained sound design: VO + music bed only, no SFX clutter

## The 6-segment template (use this for your Reels)

```
[0:00 – 0:03] HOOK
  - Ultrabold headline, 2 lines max, NO accent yet
  - Visual area empty (sets up "something will animate in here")
  - Voiceover: state the problem in one sentence

[0:03 – 0:10] BUILD-IN
  - Data/visual draws itself (Trim Path, scale-in, fade-up)
  - Headline shrinks to corner
  - Voiceover: deepens the problem with specifics

[0:10 – 0:25] MID
  - Full visualization on screen
  - Supporting caption appears
  - Voiceover: deliver the insight or key data point

[0:25 – 0:40] CLIMAX
  - Highlight zone on visual (shaded area, accent dot, etc.)
  - Word-by-word text emphasis ("the most popular thesis", "the worst year")
  - Voiceover: why this matters, the implication

[0:40 – 0:48] TRANSITION
  - Visualization fades/clears
  - Setting up CTA
  - Voiceover: "I break down the framework in..."

[0:48 – 0:54] CTA
  - Pure text card: COMMENT "[KEYWORD]"
  - Sub-line: what they get
  - Voiceover: clear instruction
```

## Animation primitives Luke Davis uses

| Primitive | AE technique | Used for |
|-----------|--------------|----------|
| Line drawing | Trim Path on Shape Layer | Stock chart traces, axis lines, underlines |
| Box scale-in | Scale 0→100% with ease-out | Logo boxes, category badges |
| Dot fade-in | Opacity 0→100% + slight scale | Data points, accent dots, bullet markers |
| Shaded area fill | Mask + Solid Color with fade-in | Highlight zones (e.g., "$70k accumulation band") |
| Text word-by-word | Text Animator with character range delay | All caption text |
| Headline shrink + reposition | Position + Scale combined keyframes | Hook headline moving to corner |

All using easing curve close to `cubic-bezier(0.55, 0, 0.45, 1)` — the
[[zajno-empirical-data]] default. None of his transitions use linear ease.

## Sound design rules

- **Voiceover + music bed only** — no sound effects, no swooshes, no clicks
- VO at sustained -17 to -19 dB
- Music ducked under VO at ~-25 dB
- Intro fade-in over first 0.5-1s (-41 dB → -19 dB)
- No silences > 0.3s — keep talking the whole time

## The CTA mechanic

Every video ends:
```
COMMENT "[KEYWORD]"
[reason — what they get]
```

This drives the Instagram algorithm via comment+save signal AND triggers a
ManyChat/Instagram-auto-DM with the offer link. Standard creator-growth pattern.

## Production stack to replicate

1. **Figma** — design static frames (use [[zajno-motion]] tokens)
2. **AE** — animate using primitives above
3. **VO record** — QuickTime or GarageBand
4. **CapCut or Premiere** — mix VO + music bed + export 1080×1920 MP4 at <50 MB
5. **Instagram** — upload as Reel

## What NOT to copy

- Don't copy his voice — record your own
- Don't reuse his music tracks — license your own (Epidemic Sound, Artlist)
- Don't replicate his exact visual style verbatim — use the *structure*, vary the *aesthetic*

## Files for reference

- Original Reels analyzed: `~/Downloads/ig-analysis/Luke Davis_*.mp4`
- Extracted audio (for listening): `~/Downloads/ig-analysis/audio/*.mp3`
- Sampled frames: `~/Downloads/ig-analysis/frames/*.jpg`
- Full memory entry: `reference_luke_davis_reels_formula_2026_05_24.md`

## When to apply this case study

Use it when building:
- Educational motion-graphics Reels
- Macro/data-driven content
- DM-funnel marketing videos
- Any short-form video that demonstrates a concept visually

Skip it for:
- Talking-head content (different format entirely)
- Screen-recording tutorials (different production pipeline)
- Vibe-driven aesthetic content (no clear pedagogical structure)
