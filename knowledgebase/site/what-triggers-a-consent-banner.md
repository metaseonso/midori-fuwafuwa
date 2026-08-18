---
title: What triggers a consent banner
tags: [site, privacy, mechanism, important]
status: settled
updated: 2026-08-19
note: informational, not legal advice
---

# What triggers a consent banner

> ⚠️ **Corrected 2026-08-19.** An earlier version of this note said the banner is triggered
> *only* by writing to the visitor's device. That is the popular version, and it is what every
> analytics vendor argues — but it is **not the legal test.** The corrected version is below.
> The practical conclusion barely changes; the reasoning does.

## The short version

**"No cookies" does not automatically mean "no banner."** But in practice, a genuinely
first-party, aggregate-only analytics setup is low-risk and no enforcement action against one has
surfaced.

## The actual test — two stages

The EU rule that created cookie banners is the **ePrivacy Directive, Article 5(3)**. The EDPB's
**Guidelines 2/2023** (adopted 7 October 2024) spell out how broadly it reaches.

### Stage 1 — does Article 5(3) apply?

Three criteria: *information* (not necessarily personal data), on *terminal equipment*, that is
either *stored* or *accessed*.

**§33 is the paragraph that catches everyone.** It states that JavaScript instructing a browser to
send asynchronous requests with targeted information *"clearly falls within the scope of Article
5(3)."*

**So every JS analytics beacon is in scope — cookies or not.** Cloudflare's, Plausible's,
Umami's, Fathom's. No vendor page engages with §33; they all argue from "we set no cookies,"
which the EDPB explicitly says is not the test.

**§54–55** adds that using an IP address to track navigation also triggers 5(3), and inverts the
burden: you must be able to *ensure* the IP did not come from terminal equipment — which for IPv6
you essentially cannot. This catches hashed-IP visitor counting (Plausible, Fathom, Umami) and
IP-based log analysis alike.

### Stage 2 — does an exemption apply?

**§56:** applicability *"does not systematically mean that consent needs to be collected."*

This is where it is won. **CNIL's audience-measurement exemption** is the load-bearing argument,
and its criteria are:

- Purpose strictly limited to measuring audience of *this* site
- Produces **anonymous statistical data only**
- Serves **exclusively the publisher's own** interests

**Disqualifiers:** cross-referencing with other processing, tracking users across multiple sites
via a shared identifier, or unified reach measurement. Retention: identifiers ≤13 months, data
≤25 months.

⚠️ **CNIL does not certify or approve analytics tools.** No such list exists. Any vendor claiming
to be "CNIL-approved" is self-certifying against published criteria.

## Where this leaves the studio

Configuration that preserves the exemption argument — and which the studio already satisfies:

- No cross-site or cross-domain tracking
- No user IDs, no per-individual events
- No rollup "unique visitors across sites"
- First-party purpose only, retention ≤25 months

**Cloudflare Web Analytics has the strongest position of any tool**, because it builds *no
per-visitor identity at all* — it counts pageviews whose referrer is a different site. There is
no hashed IP to argue about under §54–55.

## The old framing, and why it still mostly works

The popular version — *"the banner is about writing to the device, not counting the visit"* — is a
decent rule of thumb for **which tools to pick**. It correctly steers you away from cookies,
`localStorage`, and fingerprinting. It is just not the legal test, and it should not be repeated
as though it were.

| What you do | Banner needed? |
|---|---|
| Count a page view server-side, keep no identifier | ❌ No |
| Store a cookie to recognise a returning visitor | ✅ Yes |
| Read a device fingerprint to build a profile | ✅ Yes |
| Show aggregate numbers — 400 views, 60 from Korea | ❌ No |

**You can measure traffic without a banner. You just cannot follow individuals around.**

## The second rule

**GDPR** is separate, and governs *processing* personal data. An IP address counts as personal data.

Good cookieless analytics tools handle this by discarding or hashing the IP immediately and never
building a per-person profile — which is why they operate on legitimate interest rather than
requiring consent. You still **disclose** that you use them, in one line, in the privacy policy.

So the two rules resolve as:

- **ePrivacy** → don't write to the device → **no banner.**
- **GDPR** → don't retain identifiers or build profiles → **no consent needed, just disclosure.**

## Why this matters practically

It means the [[collect-nothing]] model is not a sacrifice. You still get to know whether anyone is
finding the site. You give up only the ability to track individuals, which this studio does not
want anyway.

## Related

- [[analytics-without-cookies]] — which tools satisfy this
- [[cookie-traps]] — ⚠️ things that quietly write to the device anyway
- [[collect-nothing]] — the model this enables
