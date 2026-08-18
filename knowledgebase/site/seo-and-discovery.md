---
title: SEO, discovery, and one urgent Cloudflare trap
tags: [site, seo, discovery, time-sensitive, warning]
status: research complete — contains a dated action
updated: 2026-08-19
verified: August 2026
staleness: HIGH — Google features and Cloudflare defaults change frequently. Re-verify before relying on any of it.
---

# SEO, discovery, and one urgent Cloudflare trap

> ⚠️ **Verified August 2026.** Google deprecates structured-data features constantly (FAQ died May
> 2026, HowTo 2023, sitelinks searchbox Nov 2024). **Re-check the
> [search gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)
> before building any markup.**

## 🔴 URGENT — the Cloudflare AI-bot trap

**Cloudflare replaced its single AI-bot toggle on 1 July 2026** with three separate categories:
**Search**, **Agent**, and **Training**.

> **Setting Training to "Block on all pages" also blocks Googlebot.**

Google uses overlapping infrastructure for search crawling and AI training. Blocking training with
the blunt toggle makes the site **invisible to Google Search entirely.**

⚠️ **New-domain defaults change 15 September 2026.** As of 19 August 2026 that is **27 days away**,
and `midorifuwafuwa.com` is not yet registered — so it will be a new domain landing under the new
defaults.

**The correct lever is Cloudflare's managed `robots.txt`**, which already encodes the position the
studio wants: *AI search yes, AI training no.* Use that, not the blunt block.

**Action:** when the domain is registered on Cloudflare, check the AI-bot settings before anything
else, and verify Googlebot is not blocked. Then confirm in Search Console that the site is indexable.

## The highest-value markup: image licensing

**`ImageObject` licence metadata is the only image rich result Google still has** — and it puts a
visible badge on *the studio's own artwork* in Google Images, with attribution and a link to
license it.

Two jobs at once: discovery, and staking a public provenance claim.

**Required:** `contentUrl` **plus at least one of** `creator`, `creditText`, `copyrightNotice`,
`license`.
**Recommended:** `acquireLicensePage` — this is what turns the badge into an actual enquiry.

Google also reads **embedded IPTC metadata** in the image file itself: Copyright Notice, Creator,
Credit Line, Web Statement of Rights, Licensor URL. **Embed IPTC at export time in the art
pipeline** *and* emit matching JSON-LD. Where they conflict, structured data wins.

**Why this matters more now:** Google's 25th-anniversary Images post (July 2026) announced **image
generation inside AI Overviews**. The "show me a picture of X" query is increasingly answered by
*generating* one rather than retrieving it. What remains for real retrieval is **identification and
provenance** — "who drew this, what book is this from" — which is exactly what credit and licence
metadata serves.

## Build this

| Markup | Payoff |
|---|---|
| **`ImageObject` licence metadata + IPTC** | The only image rich result. Highest value on the site. |
| **`Organization`** on the home page | Entity signal. How "Midori Fuwafuwa" becomes a *thing* rather than a string. Include `logo` (≥112×112), `sameAs`, `description`, `foundingDate` |
| **`WebSite`** with `name`/`url`/`alternateName`, root page only | Controls the site name shown in results |
| **`BreadcrumbList`** sitewide | Real rich result, cheap, still works |
| **`ProfilePage` + `Person`** on each founder page | Entity signal for the two founders |
| **Image sitemap** | Recommended when art is CDN-served. Only `<image:image>` and `<image:loc>` remain valid |
| **`Article`/`BlogPosting`** on journal posts | Better title, image and date handling |

## Emit cheaply, expect nothing

`VisualArtwork`, `BookSeries` → `hasPart` → `Book`, `CreativeWork`. No Google feature consumes
these. Their value is machine-readable description for AI grounding. Validate at
`validator.schema.org`, not the Rich Results Test.

## Do not build

- **`WebSite` + `SearchAction`** — sitelinks searchbox died November 2024
- **`FAQPage`** — died May 2026
- **`HowTo`** — died 2023
- **Book actions / `DataFeed` / `ReadAction`** — an allowlist a two-person studio will never get on
- **`ItemList`** on a gallery — carousels only support Course, Movie, Recipe, Restaurant
- **`llms.txt`** — Google explicitly says to ignore it

## The honest numbers

⚠️ **Search will not be how people find you in year one.**

- **68% of US Google searches end with no click** (Jan–Apr 2026 clickstream), up from 60% in 2024.
  Per 1,000 searches, only **276 clicks** reach the open web — down 26% in two years.
- **Only 1.74% of newly published pages reach the top 10 within a year.** Down from 5.7% in 2017.
- **73% of current top-10 pages are over three years old.** The average #1 result is five years old.
- **96.55% of indexed pages get zero Google traffic.**

**What search realistically gives you in year one:** branded and navigational queries — people who
already know the name looking you up — plus long-tail character and title names once the book
exists, plus Google Images and Lens surfacing individual artworks.

**Model the site as a conversion and credibility destination fed by social and direct** — not as a
search-acquisition asset.

## Measurement, given no analytics

With [[collect-nothing]] in force, the measurement stack is exactly two things:

1. **Google Search Console** — search and image impressions and clicks
2. **Cloudflare Web Analytics** — server-side, cookieless

⚠️ **Set up Search Console on day one. It backfills nothing** — data before verification is lost
permanently.

**And note:** AI-driven interest usually arrives as a *branded search* — someone hears about you,
then looks you up. So **the branded-query line in Search Console is the closest proxy you have for
AI and social lift.** Google folds AI Overview traffic into ordinary organic with no separate
filter; you cannot isolate it.

## One technical trap

⚠️ **Keep image URLs stable across deploys.** If the build hashes image filenames every time, every
deploy re-mints every image URL and Google starts rediscovery from scratch. Pin the hashes or use
content-stable output.

## Related

- [[measuring-arrival]] · [[collect-nothing]] · [[cookie-traps]]
- [[../craft/asset-export-rules]] — where IPTC embedding belongs in the pipeline
