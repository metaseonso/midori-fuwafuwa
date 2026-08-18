---
title: The collect-nothing model
tags: [site, privacy, principle, settled]
status: settled — founding principle
updated: 2026-08-19
note: informational, not legal advice
---

# The collect-nothing model

**Collect nothing. Then almost nothing applies.**

Every complicated obligation on the internet — consent banners, data-subject requests, deletion
rights, state-by-state privacy law, GDPR machinery — is triggered by **collecting personal data.**

A showcase site with no accounts, no forms, no tracking cookies, and no user submissions triggers
almost none of it, anywhere in the world. That is the elegant solution, and it scales globally
because it sidesteps the thing that creates jurisdiction-specific duties in the first place.

**Founder's framing:** *"Happy to be reached out to vs us trying to track everything. I have enough
of that in my life."*

This is not only a compliance strategy. It is a stance, and it matches the studio.

## What this buys

| Normally required | Here |
|---|---|
| Cookie consent banner | ❌ Not needed |
| Consent management platform | ❌ Not needed |
| Data-request / deletion process | ❌ Nothing to request |
| Breach notification readiness | ❌ Nothing to breach |
| Long privacy policy | ✅ Four short paragraphs — see [[privacy-policy-text]] |
| DMCA Designated Agent | ❌ Not needed while there are no user submissions |

## The site's scope makes this possible

Settled 2026-08-19: **the site is where people get to know the productions. It is not where they
use them.**

An introduction, not a venue. That is what keeps collect-nothing achievable permanently — the
data-heavy things live elsewhere.

## The products are a different animal — keep them separate

[[../../productions/whimsy-fairy-journal/PROJECT|Whimsy]] and the
[[../../productions/couple-app/PROJECT|Couple App]] collect **private personal data by design** —
diaries, notes, shared relationship history. Among the most sensitive data categories that exist.

**Never let the site and the products share a privacy policy, a legal footing, or an
architecture.** They are different animals with different obligations. The site stays clean; the
products carry their own weight.

## What would break this

Add any of these deliberately, never by accident:

| If you add | You now need |
|---|---|
| Tracking cookies or ad pixels | A real consent banner that blocks trackers until consent |
| A newsletter signup | Consent records, unsubscribe handling, a real privacy policy |
| A contact form | Server-side privacy basis, spam handling, retention policy |
| User accounts | Access/deletion rights, breach duties, a security posture |
| User submissions — fan art, comments | A DMCA Designated Agent ($6, renews every 3 years); without it you carry liability for what users post |
| Selling directly on the site | Payment compliance, tax handling, refund terms |
| **An AI receptionist** | ⚠️ See [[contact-without-collecting]] — this one is now on the table |
| Embedded video | ⚠️ Cookies. See [[cookie-traps]] |

## Does the Forest break this?

**No.** The [[../craft/field-and-forest|Forest]] pipeline reads the studio's *own* GitHub repos, not
visitors' data. No visitor privacy obligation attaches to it.

## Related

- [[what-triggers-a-consent-banner]] — the mechanism underneath all of this
- [[analytics-without-cookies]] — how to still see traffic
- [[contact-without-collecting]] — reach-out without data
- [[privacy-policy-text]] — the actual copy
