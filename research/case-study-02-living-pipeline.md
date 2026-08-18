---
title: "Case Study 02 — The Living Pipeline"
subtitle: "Auto-consolidating production continuity from GitHub, on a monthly and seasonal clock, without redesigning the site"
date: 2026-08-18
status: research → conclusion
---

# Case Study 02 — The Living Pipeline

## The question

Midori Fuwafuwa's productions live in GitHub repos as their working pipeline. The goal: never hand-update the site to reflect progress. Instead, on a clock — monthly, and seasonally — an automated process reviews what actually happened in a production's repo during that window, finds the story in it, and expresses that story as an immersive recap using the real assets committed during the period. The site's *template* stays fixed; only the *data* changes. This case study asks what already exists for this, and what the leading architecture would be.

*(Naming note: this living layer is the **Forest** — the companion term to Case Study 01's **Field**. A Field is the open, static-feeling space for a production; its Forest is what grows at the edge of it: a monthly sapling, a seasonal grove, a continuity that thickens over time without anyone redesigning a thing. See the reference README for how the two terms fit together.)*

---

## Part A — What already exists

Breaking the idea into its pieces, almost every piece has mature prior art on its own:

**Turning commits into structured records is fully solved.** Conventional Commits + tools like `release-please` and Changesets already parse commit history into changelogs and version bumps automatically. This is templated bullet-point output, not narrative — but it proves the *ingestion* half is a solved problem.

**Scheduling the check-in is a native GitHub feature.** GitHub Actions' `on: schedule` runs cron jobs directly against a repo, with one real operational catch worth planning around: **scheduled workflows auto-disable after 60 days of repository inactivity** and need a manual (or a cheap secondary "heartbeat") re-trigger. For a two-person studio where a production might go quiet between bursts of work, this is the one gotcha worth designing around from day one, not discovering later.

**Pulling the raw material is straightforward.** GitHub's GraphQL API can fetch commits, PRs, issues, and reviews for a date window in one shaped query; the REST commits endpoint (or actions like `tj-actions/changed-files`) can enumerate exactly which files — including images, video frames, and other binary assets — changed in that window. At a two-person studio's repo volume this sits comfortably inside GitHub's rate limits even when the query runs from inside Actions itself.

**Turning that activity into readable prose via an LLM is commodity-adjacent.** Multiple working tools already do "git log → LLM → paragraph": local CLI tools like `changeish` and `Devlog` (the latter notably reads actual source context, not just commit messages, using an agentic approach), and documented no-code pipelines (an n8n template, a fully-specified Kestra blueprint that clones a repo, runs `git log --since`, and pipes it to GPT-4o on a weekly cron) all prove this exact "cron → pull activity → LLM → distribute" skeleton works today.

**Periodic "your year/month in review" recaps of dev activity are already a small product category.** Tools like CommitRecap, Git LookBack, and GitHub's own `gh-skyline` all generate Wrapped-style periodic recaps from GitHub activity. On inspection, though, every one of them stops at **animated statistics** — commit counts, streaks, language breakdowns rendered as charts or a 3D-printable skyline — not prose narrative, and none of them draw on the project's *actual committed artwork* as illustration. The closest one, CommitRecap, uses only a GitHub avatar as its one real image; everything else is programmatically drawn.

**Storing the generated result so a static site can render it without a CMS is a solved, well-documented pattern.** A CI job can write a structured JSON/MDX file and commit it back to the repo (the standard tool for this is `git-auto-commit-action`); a static site generator's content layer — Astro's Content Collections `glob()`/`file()` loaders are built exactly for this, Eleventy's data cascade is a lighter alternative — then picks it up at build time with no traditional headless CMS involved. (Note: Contentlayer, once the default choice here, is confirmed abandoned — the ecosystem has moved to `content-collections.dev` or Velite.)

---

## Part B — The honest gap

Laying the pieces side by side makes the actual shape of the work clear:

| Piece | Maturity |
|---|---|
| Scheduled ingestion (cron, GitHub API) | Fully commodity |
| Commits → changelog bullets | Fully commodity |
| Commits → readable prose (LLM) | Commodity-adjacent, many working examples |
| Periodic "Wrapped"-style stat recap | Commodity genre, several competing products |
| **Narrative *arc* construction** — structuring a period into a story with a beginning, a turn, a resolution, tied to an ongoing fictional continuity | **No dedicated tooling found.** Every summarizer produces a flat digest, not a multi-beat arc. |
| **Selecting and sequencing real committed art/assets** to illustrate that story | **No dedicated tooling found for this exact task.** Vision-capable LLMs (Claude, GPT-4o) can tag/describe arbitrary images — a usable building block — but professional "photo culling" AI (Aftershoot, Narrative Select) solves a different problem: technical quality culling, not narrative relevance. |
| Storing generated content for a static frontend | Fully commodity |
| Rendering it as a data-driven scroll journey | Commodity as a rendering layer |

So: everything upstream (getting the data) and downstream (storing and rendering it) is genuinely off-the-shelf. **The part that's actually new is the middle** — turning a pile of commits, PRs, and images into a story with shape, and picking the right real pictures to tell it. That's good news, framed correctly: it means the interesting, defensible work is concentrated in one well-scoped place, not scattered across unsolved infrastructure.

---

## Part C — The leading architecture

Five stages, each with the current best real component and an honest note on what's install-and-go versus custom glue:

**(a) Scheduled ingestion.**
GitHub Actions `on: schedule`, one cron for monthly (e.g. `0 6 1 * *`) and one for seasonal/quarterly (`0 6 1 1,4,7,10 *`). Pull the window's activity via the GraphQL API (commits + PRs + issues + reviews in one query) and enumerate changed binary/image/video assets via the REST commits `files[]` array or `tj-actions/changed-files`. *Off-the-shelf mechanism; the query shape that isolates "new art this month" from "code this month" is simple custom glue.* Mitigate the 60-day auto-disable risk with a cheap external trigger (this environment's own scheduled-task mechanism can call the workflow via `workflow_dispatch`, sidestepping GitHub's internal schedule entirely).

**(b) Narrative synthesis + asset selection.**
An LLM call (Claude, using structured/JSON-schema-constrained output) turns the pulled activity into an ordered "scene script" — story beats, each referencing specific asset filenames/commit SHAs, rather than free text that needs re-parsing. Asset selection is the genuinely custom piece: either a two-pass approach (vision-tag each new image at ingestion time — subject, mood, which part of the Dreamland mythos it evokes — then a text synthesis pass selects and sequences from the tagged pool while writing the narrative), or a single multimodal pass feeding commit text and the actual images together. *This stage — and only this stage — is where Midori Fuwafuwa is doing real, original design work: the prompt architecture that produces a story arc instead of a digest, and the logic that picks images for narrative relevance rather than technical quality.*

**(c) Storing the result.**
A JSON manifest per production per period (`productions/<slug>/recaps/2026-08.json`): ordered scenes, each with prose, asset references, mood tag, and source links back to the real PRs/issues. The Action commits this via `git-auto-commit-action`. The real art itself never moves — it stays committed in the production's own repo (Git LFS if files get large) — the manifest just points at it. *Fully off-the-shelf pattern; only the manifest schema is a one-time design task.*

**(d) The front-end that renders it without a redesign.**
A static site generator with a content layer built for exactly this (Astro Content Collections, or Eleventy's data cascade for something lighter) reads the committed manifest. One generic "Scene" component — art + prose + mood-driven styling token — iterates over the manifest's `scenes[]` array. GSAP ScrollTrigger remains the dominant scroll-choreography primitive underneath this kind of scrollytelling; a library like `basementstudio/scrollytelling` already packages the "Root / Animation / Waypoint" component model this needs, including an image-sequence-from-stills helper that's a natural fit for turning a run of production art into a scroll-scrubbed sequence. *This is the linchpin design decision: because the template is generic and data-driven, a new month's story never touches the site's code — only its data.*

**(e) Getting it live.**
Because step (a)'s commit already pushes to the repo, a normal connected host (Cloudflare Pages, Vercel, Netlify) rebuilds on that push with no extra plumbing. If an editorial pause before publishing feels right for a two-person studio putting out an AI-authored story under their own name, route the generated manifest to a PR instead of `main`, and let merging that PR — a five-second human glance, not a redesign — be the actual publish trigger.

---

## Conclusion — what to build vs. what to install

The leading architecture is not a research problem, past one deliberately narrow point: ingestion, storage, and rendering are all genuinely solved by existing, well-maintained tools (GitHub Actions, the GitHub API, Astro's content layer, `git-auto-commit-action`, GSAP-based scrollytelling). Midori Fuwafuwa doesn't need to build a pipeline framework — it needs to wire five known-good components together, which is an afternoon of integration work, not a systems project.

The one place real design effort belongs is the narrative-and-asset-selection stage — and it's worth treating that as its own small, ongoing craft project rather than a "prompt once and forget" task, since it's the part with no off-the-shelf answer to fall back on. Two practical recommendations follow directly from the novelty assessment:

1. **Separate the tagging pass from the storytelling pass.** Tag new committed assets for mood/subject/mythos-relevance as they arrive (cheap, incremental), so the monthly/seasonal synthesis call is choosing from an already-curated pool rather than reasoning about raw images cold. This keeps the expensive, careful reasoning step focused on arc construction, which is the actually-hard part.
2. **Keep a human glance in the loop at first.** Route each generated recap through a PR rather than straight to production, at least until the narrative voice is dialed in — cheap insurance against an AI-authored story misreading a quiet month or a messy one, and it costs nothing against the "no manual redesign" goal, since approving a PR isn't redesigning anything.

Framed against Case Study 01: this living pipeline is exactly the "behind the scenes" destination that case study recommended keeping separate from the front page — the Forest that grows at the edge of each production's Field, letting the front page stay minimal and mystique-forward while still being genuinely, continuously alive underneath. One optional visual idea worth carrying into the build: let the Forest literally thicken over time — a new sapling/tree per monthly consolidation, a fuller grove per season — so the metaphor and the data structure (one manifest entry per period) match exactly.

---

## Sources

**Changelog automation & scheduling**
- [GitHub Docs — Events that trigger workflows (schedule)](https://docs.github.com/actions/using-workflows/events-that-trigger-workflows)
- [GitHub Docs — Rate limits for the GraphQL API](https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api)
- [GitHub Docs — REST API endpoints for commits](https://docs.github.com/en/rest/commits/commits)

**LLM-driven narrative/changelog tools**
- [Kestra blueprint — Summarize Weekly Git Commits with OpenAI](https://kestra.io/blueprints/ai-summarize-weekly-git-commits)
- [Devlog — an AI-powered developer journal](https://dev.to/zeshama/devlog-i-built-an-ai-powered-developer-journal-that-turns-git-commits-into-stories-3fdl)
- [changeish — local-first AI changelog CLI](https://github.com/itlackey/changeish)

**"Wrapped"-style recap prior art**
- [CommitRecap](https://towardsai.com/p/machine-learning/i-built-commitrecap-so-your-github-year-reads-like-a-story)
- [Git LookBack](https://www.gitlookback.dev/)
- [github/gh-skyline](https://github.com/github/gh-skyline)
- [git-story (PyPI)](https://pypi.org/project/git-story)

**Git-as-CMS / static content pipelines**
- [Astro Docs — Content collections](https://docs.astro.build/en/guides/content-collections/)
- [Eleventy Docs — Data Cascade](https://www.11ty.dev/docs/data-cascade/)
- [stefanzweifel/git-auto-commit-action](https://github.com/stefanzweifel/git-auto-commit-action)
- [Wisp — Contentlayer has been abandoned, alternatives](https://www.wisp.blog/blog/contentlayer-has-been-abandoned-what-are-the-alternatives)

**Structured LLM output & vision**
- [Anthropic — Structured outputs on the Claude Developer Platform](https://tessl.io/blog/anthropic-brings-structured-outputs-to-claude-developer-platform-making-api-responses-more-reliable)
- [Claude Vision API — production guide](https://www.developersdigest.tech/blog/claude-vision-api-production-guide)

**Scrollytelling front-end**
- [basementstudio/scrollytelling](https://github.com/basementstudio/scrollytelling)
- [The Pudding — How to implement scrollytelling with six different libraries](https://pudding.cool/process/how-to-implement-scrollytelling/)

**Deploy triggers**
- [Cloudflare Pages — Deploy hooks](https://developers.cloudflare.com/pages/configuration/deploy-hooks/)

*(Full annotated source list from the research pass is available in this session's transcript — this file keeps only the primary references.)*
