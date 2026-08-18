---
title: Analytics without cookies
tags: [site, analytics, tooling, settled]
status: settled — Cloudflare Web Analytics
updated: 2026-08-19
note: informational, not legal advice
---

# Analytics without cookies

**Decision: Cloudflare Web Analytics. Google Analytics is out.** Settled 2026-08-19.

Why this works without a banner: [[what-triggers-a-consent-banner]].

## The choice

### ✅ Cloudflare Web Analytics — use this, but check one thing first

- **Free**, no traffic limits. One-click enable on Cloudflare Pages, auto-injected on next deploy.
- No cookies, no client-side storage — and uniquely, **no per-visitor identity at all.** It counts
  pageviews whose referrer is a different site. There is no hashed IP, which gives it the
  strongest legal position of any tool here (see [[what-triggers-a-consent-banner]] §54–55).
- Adds no new processor — Cloudflare is already the host.

⚠️ **Verify before committing: does it show UTM parameters?** Cloudflare's FAQ states it *"does
not log query strings to avoid collecting potentially sensitive data."* If that holds, **you
cannot see which campaign or channel sent someone** — which guts the main way to answer "how do
people find us." Check the Dimensions view in the dashboard on day one.

**If UTMs are not visible → switch to Plausible ($9/mo).** Two things it gives you that Cloudflare
does not: full UTM reporting, and a verified **"AI assistants" channel** that reports traffic from
ChatGPT, Claude, Perplexity, Copilot, Gemini, DeepSeek and Grok by name. Given that AI referral is
a real and growing arrival path, that visibility may be worth $9.

⚠️ **A footnote on "no cookies at all":** Cloudflare *as a CDN* may set `__cf_bm` (bot management),
`cf_clearance` (challenges), or `_cfuvid` (rate limiting) depending on which features are enabled.
Web Analytics sets none of them, but the site may still carry them. They are documented as
strictly necessary, so no banner — but do not claim the site sets zero cookies without checking.

### Good paid alternatives, if nicer reporting is ever wanted

| Tool | Cost | Notes |
|---|---|---|
| **Plausible** | ~$9/mo | Cookieless, EU-hosted, very clean UI. Self-hostable free. |
| **Fathom** | ~$15/mo | Cookieless, EU-hosting option. |
| **Umami** | Free, self-hosted | Open source. Free if you run it yourself. |

These differ in polish and price, not in legal position.

### ❌ Google Analytics — avoid

- **Uses cookies** → forces a real consent banner.
- Visitors who decline become invisible, so the numbers are wrong anyway.
- Repeated EU legal trouble over data transfers to the US.
- Free in money, expensive in compliance.

For a site whose whole model is [[collect-nothing]], it is the wrong tool.

## What you get

- Page views, and which pages
- Referrers — where visitors came from
- Country
- Device type: phone, tablet, desktop
- Trends over time

That answers everything that matters: *Is anyone finding us? From where? What are they reading? Is
it growing?*

## What you give up

- Following one person across sessions
- Inferring age, gender, interests
- Ad-campaign attribution

None of it serves this site.

## Server logs — you already have these

Whatever hosts the site records requests — IP, time, page, browser — whether you want it or not.

Keep it simple: **do not use logs to profile individuals, and keep retention short.** One line in
the privacy policy covers it. See [[privacy-policy-text]].

## Related

- [[what-triggers-a-consent-banner]] — the mechanism
- [[cookie-traps]] — ⚠️ what can undo this
- [[privacy-policy-text]] — what to disclose
