---
title: Measuring arrival without tracking people
tags: [site, analytics, attribution, arrival]
status: settled approach
updated: 2026-08-19
note: informational, not legal advice
---

# Measuring arrival without tracking people

The site's job is building an audience. So the one question worth answering is **"where did they
come from?"** — not "who are they."

Those turn out to be separable, which is the good news.

## What the referrer header actually gives you

Browsers default to `strict-origin-when-cross-origin` (since November 2020).

| Navigation | What you receive |
|---|---|
| Same-origin | Full URL, path and query |
| Cross-origin HTTPS → HTTPS | **Origin only** — `https://bsky.app/`, never the post path |
| HTTPS → HTTP | **Nothing** |

**So you can answer "did Bluesky send anyone?" You can never answer "which Bluesky post?"** from
the referrer alone.

**Things that arrive as "Direct" with no referrer at all:** email clients, RSS readers, messaging
apps, bookmarks, typed URLs, QR codes, in-app browsers, and most AI chat interfaces. The Direct
bucket is not a channel — it is a blind spot.

## UTMs do not violate the no-tracking stance

This is the key insight, and it is worth being precise about:

> **A UTM parameter is a property of the LINK, not the PERSON.**

`?utm_source=newsletter&utm_campaign=2026-08` is byte-identical for every single person who
receives it. It carries no per-user identifier. It stores nothing on the device. It cannot be
joined back to an individual.

It answers **which channel** without ever answering **who**. That is entirely consistent with
[[collect-nothing]].

⚠️ **The line not to cross:** per-recipient tokens like `?uid=abc123`. Those *are* person-level and
would break the stance. Never generate them.

## The approach

**1. Tag every link the studio controls.**

```
utm_source=bluesky | tumblr | newsletter | rss | instagram
utm_medium=social | email | feed
utm_campaign=2026-08-kits-reveal
```

Campaign-level only. Never per-person.

**2. Per-channel landing pages — the robust backstop.**

`/hello-bluesky`, `/from-the-newsletter`, `/zine`

This works with **zero referrer and zero query string**, which makes it the only technique that
survives regardless of which analytics tool you pick — including if Cloudflare Web Analytics turns
out not to log query strings. It is also the most human option: each page can actually greet the
person who arrived.

**3. QR codes → a dedicated path, not a UTM.**

QR scans carry no referrer at all. Print material (a zine, a card at an event) should point at its
own short path.

**4. Short links only if self-hosted.**

A Cloudflare Worker redirect is fine. A third-party shortener adds a processor and a tracking
surface for no benefit.

**5. Ask, once.**

"Where did you hear about us?" answered by a human beats any amount of inference about the Direct
bucket. This fits the studio's stance better than analytics does.

## Newsletter: no open-tracking pixels

⚠️ If a newsletter ever ships, **do not enable open tracking.** Tracking pixels sit squarely inside
the ePrivacy scope discussed in [[what-triggers-a-consent-banner]], and CNIL published a specific
recommendation on email tracking pixels in **May 2026**.

Tag the **links** with campaign-level UTMs instead. Click data by campaign is enough, and it does
not require a pixel in anyone's inbox.

## AI referrals

Traffic from AI assistants is real and growing, and it attributes unusually well — ChatGPT appends
`?utm_source=chatgpt.com` to links it cites in web-search mode, so it lands correctly even when the
referrer is stripped.

**Plausible reports these as a named "AI assistants" channel** (ChatGPT, Claude, Perplexity,
Copilot, Gemini, DeepSeek, Grok). Cloudflare Web Analytics does not.

⚠️ **Google AI Overviews are invisible.** Google folds AI-feature traffic into ordinary organic
search in Search Console, with no separate filter. You cannot separate it. And AI-driven interest
often arrives later as a **branded search** — someone hears about you, then searches your name —
so the branded-query line in Search Console is the closest proxy you have for AI and social lift.

## What you can and cannot know

| | |
|---|---|
| ✅ Reliable | Platform level — "Bluesky sent 120, ChatGPT sent 40, Direct is 55%" |
| ⚠️ Only with UTMs | Post or campaign level — which post, which newsletter issue |
| ❌ Impossible, by design | Person level — repeat visits, cross-channel journeys |

That last row is the point, not a limitation.

## Related

- [[analytics-without-cookies]] · [[what-triggers-a-consent-banner]] · [[collect-nothing]]
