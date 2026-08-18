---
name: zajno-motion
version: 1.0.0
description: |
  Zajno-style motion design playbook — 8 principles from motion.zajno.com codified
  as a reusable skill. Covers easing, offset/delay (stagger), fade, transform/morph,
  masking, dimension, parallax, and zoom. Ships with production-ready GSAP + Lenis +
  Lottie + ScrollTrigger snippets and Zajno's actual custom-bezier easing curves
  ("bounce" and "bounceSmall") extracted from their site source.
  Use when asked to "add motion", "make this feel premium", "Zajno-style animation",
  "scroll animation", "stagger reveal", "smooth scroll", or building any landing-page
  micro-interaction. Proactively suggest when a page has static reveals or feels flat.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# Zajno Motion — Skill Entry Point

This skill codifies the motion-design playbook published by Zajno Digital Studio
at https://motion.zajno.com, plus the technical recipe extracted from their
production source code.

## When to invoke

- User asks for motion / animation / "premium feel" on a web project
- User mentions Zajno, motion.zajno.com, or "studio-grade animation"
- User has a static page and wants scroll-triggered reveals
- User asks about easing curves, stagger timing, parallax, or smooth scroll
- A code review surfaces flat, instant transitions that should be eased

## The 8 principles (one file each in `principles/`)

| # | Principle              | Use it for                                                |
|---|------------------------|-----------------------------------------------------------|
| 1 | Easing                 | Every transition. Linear is the enemy.                    |
| 2 | Offset & Delay         | Multiple elements appearing — never simultaneously.       |
| 3 | Fade In/Out            | Always combined with position/scale — never alone.        |
| 4 | Transform & Morph      | Shape-to-shape continuity, keeps focus.                   |
| 5 | Masking                | Reveals with personality; morphed shapes as windows.      |
| 6 | Dimension              | Depth via layered motion, not skeuomorphic shadows.       |
| 7 | Parallax               | Spatial illusion; farther = slower.                       |
| 8 | Zoom                   | Inter-state transitions communicating depth + hierarchy.  |

Read them in `principles/01-easing.md` … `principles/08-zoom.md`.

## How to apply this skill

1. **Read the principle file(s) that match the task.** Each one has the
   "what / why / how / anti-pattern" structure.
2. **Pull the matching snippet from `examples/`.** All examples are
   production-ready (no pseudo-code) and use the same stack Zajno uses.
3. **Use the values in `references/timing-system.md` and
   `references/easing-curves.md`.** These come from Zajno's actual source —
   not made up.
4. **Run the `checklist.md` quality gate before declaring done.**

## Stack assumed

The snippets use GSAP 3.10+, ScrollTrigger, CustomEase, Lenis (smooth scroll),
and optionally Lottie + Matter.js. See `references/tech-stack.md` for install
commands and CDN URLs. If the project uses Framer Motion or another lib,
`references/framer-motion-port.md` shows how to translate the principles.

## Empirical data — read this when in doubt

`references/zajno-empirical-data.md` is the most important reference doc.
It is parsed directly from **27 Lottie files** served by motion.zajno.com
(7,897 keyframes total). It tells you:

- Their actual default easing curve (`cubic-bezier(0.55, 0, 0.45, 1)`)
- Their exact UI duration (0.67s) and showcase duration (2.35s)
- Their full color palette (mostly ink + warm off-white + one blue-purple accent)
- Their layer-complexity budget per scene
- File-size budget for a landing page

The raw Lottie files live in `~/.cache/zajno-motion/lotties/` — outside
the skill so the skill stays light/distributable. Open any of them in
[Lottielab](https://www.lottielab.com) or LottieFiles editor to watch
the actual animations.

## Storage architecture

| Tier | Location | Role |
|------|----------|------|
| Skill (this folder) | `~/.claude/skills/zajno-motion/` | `.md` knowledge + `empirical-output.json` + parser + scripts. ~165 KB, distributable. |
| Local cache | `~/.cache/zajno-motion/` | Raw Lottie files (`lotties/`) + page source archive (`source/`) + `manifest.json` + refresh logs. ~1.4 MB, per-machine. |
| Semantic memory | `memory-search` MCP | Learnings + diffs over time. Only material changes. |

### Cache layout

```
~/.cache/zajno-motion/
├── lotties/                  # 27 Lottie animation JSON files (~1.2 MB)
├── source/                   # Page source time-capsule (~172 KB)
│   ├── index.html            # The full motion.zajno.com page
│   └── script.v33.min.js     # Their custom GSAP+Lenis+Lottie wiring
├── manifest.json             # sha256 per file, first_seen/last_changed timestamps
├── last-diff.md              # Set by refresh.sh if material change. Claude reads + clears.
├── takedown-detected.md      # Only present if site unreachable. Claude reads + deletes.
└── refresh.log               # launchd stdout/stderr from quarterly job
```

If motion.zajno.com ever goes down for good, everything above survives.
The skill remains fully functional with the archived data.

## ALWAYS check for refresh signals on activation

When this skill is invoked, check these two files first:

### `~/.cache/zajno-motion/last-diff.md`
If non-empty, a scheduled refresh detected material changes to Zajno's
site that haven't been processed yet:

1. Read the diff content
2. Use `mcp__memory-search__write_memory` to record what changed
   (one memory entry, type `project`, name pattern `zajno_motion_change_YYYY_MM_DD`)
3. Truncate `last-diff.md` to empty so we don't double-record

### `~/.cache/zajno-motion/takedown-detected.md`
If present, motion.zajno.com was unreachable on the last refresh attempt.
The cache still has the last-known-good data — the skill is fully functional.

1. Read the file (it has the date + HTTP status)
2. Write a memory entry: type `project`,
   name `zajno_motion_takedown_YYYY_MM_DD`
3. Delete the file so we don't keep alerting

If both files are empty/missing, no action needed — proceed with the user's task.

## Refresh pipeline

Run a refresh manually any time:

```bash
bash ~/.claude/skills/zajno-motion/scripts/refresh.sh
```

Quarterly automation via launchd (the user installs this once):

```bash
bash ~/.claude/skills/zajno-motion/scripts/install-cron.sh install   # one-time
bash ~/.claude/skills/zajno-motion/scripts/install-cron.sh status    # check
bash ~/.claude/skills/zajno-motion/scripts/install-cron.sh run-now   # ad-hoc trigger
bash ~/.claude/skills/zajno-motion/scripts/install-cron.sh remove    # uninstall
```

The job fires on Jan 1, Apr 1, Jul 1, Oct 1 at 09:13 local.

## Skill type

**Flexible.** The principles are not a checklist to execute top-to-bottom —
they are a vocabulary. Pick the ones that fit. The anti-patterns matter more
than the timing values: ship one well-eased reveal over six clumsy ones.

## Distribution

This skill is self-contained. To share with a teammate:

```bash
# Copy the whole folder
cp -R ~/.claude/skills/zajno-motion /path/to/teammate/.claude/skills/

# Or commit it to a shared dotfiles repo
cd ~/.claude/skills/zajno-motion && git init && git add . && git commit -m "Zajno motion skill v1.0.0"
```

See `INSTALL.md` for plugin-style distribution (manifest, versioning).

## Source

- Principles: https://motion.zajno.com (Zajno Digital Studio)
- Technical recipe: extracted from `cdn.zajno.com/dev/motion/script.v33.min.js`
  on 2026-05-23
- Custom easing curves: lifted verbatim from production source

## Credit

All eight principles are Zajno's published work. This skill is a structured
re-presentation of public material with code recipes derived from their
publicly-served front-end source. Use it to *learn the vocabulary* — don't
just copy their site.
