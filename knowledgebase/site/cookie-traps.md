---
title: ⚠️ Cookie traps
tags: [site, privacy, warning, gotcha]
status: flagged — know these before building
updated: 2026-08-19
note: informational, not legal advice
---

# ⚠️ Cookie traps

Things that quietly write to a visitor's device and undo a cookie-free site. Each one, on its own,
would force a consent banner onto a site that otherwise needs none.

## The big one: embedded video

**An embedded YouTube player will drop a tracking cookie onto your cookie-free site.** It does this
on page load, before anyone presses play.

Founder's call: **no YouTube.** Settled 2026-08-19.

If video is ever needed anyway, two safe routes:

1. **`youtube-nocookie.com`** — YouTube's privacy-enhanced embed domain. Defers cookies until
   playback. Better, though not perfectly clean.
2. **Click-to-load poster** — show a static image; only load the actual player when the visitor
   clicks. Nothing touches their device until they choose it. **This is the clean option**, and it
   is also faster, since you avoid loading a heavy third-party player on every page view.

Self-hosting the video file, or using a privacy-respecting host, avoids the problem entirely.

## The rest of the list

| Trap | What it does | Safe alternative |
|---|---|---|
| **Google Fonts (hosted)** | Requests fonts from Google's servers, exposing visitor IPs to a third party. Ruled a GDPR issue in German courts. | **Self-host the WOFF2 files.** The design system already specifies self-hostable OFL fonts. |
| **Embedded maps** | Google Maps sets cookies | Static map image, or a plain link |
| **Social embeds** — X, Instagram, Facebook | Set tracking cookies, often aggressively | Screenshot plus a plain link |
| **Ad pixels** — Meta, Google Ads | Tracking by definition | Don't. See [[collect-nothing]] |
| **A/B testing tools** | Usually cookie-based | Don't, at this scale |
| **Comment systems** — Disqus and similar | Heavy third-party tracking | No comments; see [[collect-nothing]] |
| **CDN-hosted JS libraries** | Third-party requests expose visitor IPs | Bundle and self-host |
| **Chat widgets** | Session cookies, third-party data flow | ⚠️ See [[contact-without-collecting]] |

## The general rule

**Anything loaded from a domain you don't control is a potential trap.** Self-host fonts, scripts,
and styles. Third-party requests are the mechanism, and self-hosting closes it.

This also happens to make the site faster — fewer DNS lookups, fewer connections, no third-party
render blocking. The privacy-preserving path and the fast path are the same path again.

## Related

- [[what-triggers-a-consent-banner]] — why these matter
- [[collect-nothing]] — the model these would break
- [[../craft/efficient-motion]] — the same self-host-everything logic, for performance
