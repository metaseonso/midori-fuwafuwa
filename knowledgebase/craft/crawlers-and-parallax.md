---
title: ⚠️ Crawlers vs parallax — build constraints
tags: [craft, seo, build, warning, important]
status: research complete — these are hard build rules
updated: 2026-08-19
verified: August 2026
staleness: MEDIUM-HIGH — crawler behaviour changes; the AI-crawler measurements are from Dec 2024 and Dec 2025. Re-verify before launch.
---

# ⚠️ Crawlers vs parallax — build constraints

> ⚠️ **Verified August 2026.** Google's docs change constantly and the broadest AI-crawler
> measurement available is from **December 2024** — 20 months old. Treat the "AI crawlers don't
> render JS" finding as the last good measurement, not as guaranteed current fact.

These constrain [[the-dreamland]] directly. A scroll-driven parallax site has specific, documented ways
of becoming invisible.

## The two sentences that govern everything

> **"Google Search does not interact with your page."**
> — Google's lazy-loading documentation, December 2025

Googlebot **does not scroll and does not click.** So anything that only exists after a scroll event
does not exist at all.

> **No major AI crawler renders JavaScript.**
> — Vercel + MERJ, network-wide measurement

GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, CCBot, Amazonbot, Meta's crawlers: **none execute
JS.** They read the raw HTML and nothing else. Only **Googlebot** and **Applebot** render.

## 🔴 The 100vh trap — the one most likely to bite this site

Googlebot renders at a fixed viewport, **then expands the viewport height to match the whole page.**
It does not scroll; it grows.

**What that does to a full-screen hero:**

> An uncapped `100vh` hero **recalculates against the expanded viewport** and can become thousands
> of pixels tall. Real content gets pushed catastrophically far down. And lazy-loaded content
> beneath it may never trigger, because the crawler never "reaches" the activation threshold.

**The fix:**

```css
.hero {
  min-height: 100svh;
  max-height: 900px;   /* the cap is the whole point */
}
```

**Cap every fullscreen element.** For a site whose front door is a full-viewport dream world, this
is not optional.

## The reveal-animation problem

The standard parallax pattern — content at `opacity: 0`, revealed on scroll — fails twice:

1. **Googlebot never scrolls**, so it indexes a DOM where the content sits at `opacity: 0`.
2. **Google's spam policy lists `opacity: 0` among hidden-text examples.** Legitimate uses
   (accordions, sliders, tooltips) are explicitly permitted, and the abuse test is "solely to
   manipulate search engines" — so this is a risk zone, not a violation. Still worth avoiding.

**The fix — hide only when JS is present:**

```html
<script>document.documentElement.classList.add('js')</script>
```
```css
html.js .reveal { opacity: 0; transform: translateY(24px); }

@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1 !important; transform: none !important; }
}
```

Now every no-JS client — and every case where GSAP fails to load — sees fully visible content. The
reduced-motion block is a second safety net, and it is required anyway by
[[reduced-motion-first]].

## Hard rules for the build

### Content must exist in the HTML

- **Use ScrollTrigger for animation only, never for content existence.** No
  `onEnter: () => injectSection()`. Sections exist in the HTML; ScrollTrigger only animates them.
- **Never build galleries from a JS array at runtime.** Iterate the data in Astro frontmatter at
  build time so real `<img>` tags land in the output.
- **No `client:only`** on anything containing indexable content. It skips server rendering
  entirely. Use `client:visible` — same server HTML, deferred hydration only.

### The 2 MB cap

> Googlebot crawls **the first 2 MB of each resource, uncompressed**, then stops.

A bundled `gsap + ScrollTrigger + Lenis + three.js` chunk over 2 MB gets **truncated mid-file** →
syntax error → blank render. **Split the chunks and check `dist/_astro/*.js` sizes at build.** HTML
documents are capped at 2 MB too.

### WebGL is invisible

Google's docs state plainly that **Googlebot does not support WebGL.** Anything whose only
representation is inside a canvas does not exist to search. The design system already reserves
WebGL for a single decorative accent — keep it decorative, never load-bearing.

### Smooth scroll must be additive

Lenis and Locomotive virtualise scrolling by transforming a wrapper, often with
`body { overflow: hidden }`. **The page must be fully readable and scrollable with the library
removed.** Add `overflow: hidden` from JS after init — never in the base stylesheet, and never wrap
content in a `transform: translate3d(...)` container in the static HTML.

### Other traps

- **No hash-fragment routing** (`#/fields/the-kits`). The AJAX-crawling scheme has been dead since
  2015 and Google's docs carry an explicit bad example of exactly this. Real `<a href>` to real
  prerendered URLs.
- **No localStorage gating.** Googlebot clears storage and cookies between page loads, so a
  "seen the intro" flag is **never** set — it sees the first-visit state on every render. An intro
  splash that hides the site would hide it permanently from Google.
- **`loading="lazy"` is fine and recommended** — but never on the hero/LCP image, and the real URL
  must be in `src`, not only `data-src`.
- **`content-visibility: auto`** — no Google documentation exists either way. Probably safe (the DOM
  is intact), but verify in URL Inspection after adding it. Never `content-visibility: hidden` on
  indexable content.

## Alt text is doing double duty now

> For every AI crawler, the `alt` text **is** the artwork. It is the only description they will ever
> ingest, because they never render the image and never run the lightbox.

This changes what alt text is for on an illustration site. It is no longer only an accessibility
obligation — it is the entire machine-readable description of the studio's work.

**An image whose only caption lives in a JS-driven lightbox is invisible to GPTBot, ClaudeBot and
PerplexityBot.** Put real `<figcaption>` in the HTML.

## Verification loop

1. **`curl` as a bot** and read the raw output:
   ```bash
   curl -A "GPTBot" https://midorifuwafuwa.com/ | grep -c "<img"
   ```
   **If a human can read the page from `curl` output alone, every AI crawler can too.** One test
   covers GPTBot, ClaudeBot, PerplexityBot, CCBot and the rest simultaneously.
2. **URL Inspection → Test live URL → View rendered HTML.** Confirm every artwork `<img src>` is
   present, the `<h1>` is present, and nothing you care about is stuck at `opacity: 0`.
3. **Google's own scroll-diff script** — `lazyimages_without_scroll_events.js` from
   GoogleChromeLabs/puppeteer-examples. It diffs a scrolled versus non-scrolled render and reports
   exactly what a non-scrolling client misses. **The single best automated check for a parallax
   site.**
4. **Simulate the expanded viewport manually.** DevTools → custom device at 1024 × 8000 → hard
   reload without scrolling → screenshot. This exposes the 100vh trap and any unfired reveals
   immediately.
5. **Whitelist `Google-InspectionTool`** in Cloudflare, or URL Inspection goes dark and you lose
   your only real debugging tool.

## robots.txt — search yes, training no

⚠️ **See [[../site/seo-and-discovery]] for the urgent Cloudflare AI-bot setting** that can block
Googlebot entirely.

Two things worth knowing when writing the file:

- **`Google-Extended` and `Applebot-Extended` are not crawlers.** They are robots.txt tokens that
  control training use only. Both vendors state explicitly that disallowing them **does not affect
  search inclusion.** Blocking them costs nothing.
- **Distinguish AI-*search* crawlers from AI-*training* crawlers.** `OAI-SearchBot`,
  `Claude-SearchBot` and `PerplexityBot` drive citations and referral traffic. `GPTBot`,
  `ClaudeBot`, `CCBot` and `Bytespider` are training. Blocking the first group by accident costs
  real visibility.
- **User-triggered fetchers ignore robots.txt** by their vendors' own statements — `ChatGPT-User`,
  `Perplexity-User`, `Claude-User`.

## Related

- [[the-dreamland]] — the design these constrain
- [[efficient-motion]] · [[reduced-motion-first]] · [[asset-export-rules]]
- [[../site/seo-and-discovery]] — ⚠️ the urgent Cloudflare item
