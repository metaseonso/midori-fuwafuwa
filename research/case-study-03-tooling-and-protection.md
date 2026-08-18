---
title: "Case Study 03 — Tooling Fit & Studio Protection"
subtitle: "Which Claude Skills actually fit the Fields/Forests plan, and what makes the studio's work and business genuinely protected"
date: 2026-08-18
status: research → conclusion
---

# Case Study 03 — Tooling Fit & Studio Protection

Two unrelated but equally practical questions, asked together because both need answering before real build work starts: which tools should Claude Code actually reach for, and what does "fully protected" mean for an artistically-forward, two-person studio with mixed hand-drawn and AI-assisted work.

---

# Part A — Claude Skills fit assessment

## What a Claude Skill is, mechanically

A skill is a folder with a `SKILL.md` that Claude Code loads progressively — a short description stays in context always, full instructions load only when relevant, bundled scripts/references load only when touched. Skills live at four levels (personal, project, enterprise, or plugin-installed via a marketplace) and follow an open spec, so they're portable. One mechanic worth knowing for the Forest pipeline specifically: a SKILL.md can embed a live shell command whose output gets spliced into context before Claude sees it — useful for prototyping the "pull GitHub activity" step interactively before it's locked into a scheduled Action.

Source: [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills)

## The landscape, honestly

**Official** (Anthropic-maintained, `github.com/anthropics/skills`, 17 skills total): `frontend-design`, `canvas-design`, `algorithmic-art`, `theme-factory`, `brand-guidelines`, `docx`/`pdf`/`pptx`/`xlsx`, `mcp-builder`, `claude-api`, `webapp-testing`, `web-artifacts-builder`, `doc-coauthoring`, `internal-comms`, `slack-gif-creator`, `skill-creator`.

**Community**, verified by reading actual SKILL.md content rather than trusting directory listings: `freshtechbro/claudedesignskills` (719★, MIT, "production" status — `gsap-scrolltrigger`, `threejs-webgl`, `locomotive-scroll`, and others), `alexejluft/brudi`'s `orchestrating-gsap-lenis`, `spillwavesolutions/publishing-astro-websites-agentic-skill` (28★, single author — verify against current Astro docs before trusting), `onewave-ai`'s `accessibility-auditor` (168★), `ComposioHQ/awesome-claude-skills`' `changelog-generator`. One large marketplace (`jeremylongshore`, claiming 3,069 skills) is real in scale but uneven in quality — templated, auto-generated descriptions show up repeatedly — treat it as a haystack to search, not a trusted default.

Source: [github.com/anthropics/skills](https://github.com/anthropics/skills)

## Mapped to the plan

**Fields (the frontend build):**
`frontend-design` fits directly — it forces deliberate type/color/motion choices and actively fights generic "AI-slop" output, which matters because the whole point of a Field is a specific chibi register, not a template look. `gsap-scrolltrigger` and `threejs-webgl` (freshtechbro) are solid production-grade reference material for the choreography and sparing-WebGL layers — but neither mentions native CSS `scroll-timeline` or `prefers-reduced-motion`, which Case Study 01 makes the *primary* mechanism and a first-class requirement, so treat them as supplementary, not authoritative, on those two points. `orchestrating-gsap-lenis` is narrow but exactly on-target: it fixes the specific, well-known GSAP+Lenis animation-frame conflict this stack will hit. `publishing-astro-websites-agentic-skill` matches the content-layer approach Forests depends on, but is low-maturity — use as a reference, verify against current docs. `webapp-testing` and `accessibility-auditor` both fit the "verify it actually works and stays accessible" step directly.

**Forests (the living pipeline):**
`claude-api` is the clearest match in the entire landscape — it documents exactly the structured/JSON-schema output mechanic the narrative-synthesis step needs, and it's bundled by default, auto-triggering the moment an Anthropic SDK shows up in the project. `changelog-generator` (community) is the closest existing analog and worth reading as a pattern reference, but its output contract doesn't fit: flat markdown, no image handling, release-notes framing rather than a period narrative arc — it confirms rather than replaces Case Study 02's finding that this step is custom work. `mcp-builder` is plausible but not load-bearing — the pipeline as designed is one-shot scripted API calls inside a scheduled Action, not a persistent server; it would only matter if the studio later wants an interactive "ask about repo activity" tool inside Claude Code sessions generally.

**General / meta:**
`skill-creator` is high-value here specifically because both prior case studies converged on the same finding — the narrative-arc-and-asset-curation step has no off-the-shelf tool — which makes it worth turning into a durable, testable custom skill rather than re-deriving the prompt every session. The same tool is the natural way to build a "Midori Fuwafuwa brand" skill that keeps every future session on-palette and on-model without repeating instructions; `brand-guidelines` (Anthropic's own, hardcoded to Anthropic's palette) is a usable *structural template* for that, not a usable skill as-is. `icon-designer` transfers a useful discipline (stroke-weight and grid consistency) to a chibi asset library even though it's built for app icons. `canvas-design` and `algorithmic-art` are usable for one-off key art and ambient generative accents, but both default toward a "museum-quality, sophisticated" register that runs against "cute and fluffy" — expect to override their default aesthetic instructions every time, not just once.

## Overlaps and disqualifications

- **`web-artifacts-builder` — disqualified for the core build.** It bundles a React/Vite app into one self-contained HTML file for Claude.ai artifact sharing. That's a different deliverable shape entirely from a real multi-page Astro/Eleventy site with its own repo, CI, and deploy target — using it would mean fighting its bundling assumptions the whole way.
- **`locomotive-scroll` (freshtechbro) — disqualified by a decision already made.** Both it and Lenis solve the same problem; Case Study 01 already chose Lenis specifically because it works *with* native scroll rather than hijacking it. Installing this skill only invites a second, inconsistent smooth-scroll implementation.
- **`theme-factory` — disqualified as a process, not just a palette mismatch.** Its workflow assumes picking from 10 pre-built themes; none is chibi/fluffy, and more fundamentally the studio doesn't need to *pick* a theme, it needs to *always enforce* its one already-defined theme — which is what a custom brand skill (built via `skill-creator`, patterned on `brand-guidelines`) does instead.
- **`canvas-design` / `algorithmic-art` vs. `frontend-design`** — no real conflict (different deliverable types), but all three share a "write a design philosophy first" method, and the first two default toward a more "sophisticated minimalist" register than this brand wants. Not disqualified, just needs active steering every time.
- **`mcp-builder`** — not disqualified, just not required by the architecture as specified; a nice-to-have for later, not a day-one need.

## Priority order

1. **`claude-api`** — free (bundled), and it's the one skill mapped onto a hard technical requirement already locked into the Forests plan.
2. **`skill-creator`** — highest leverage: turns the one genuinely custom piece of this whole project (narrative-arc synthesis) and the recurring brand-consistency need into durable, reusable assets instead of ad hoc re-explaining.
3. **`webapp-testing`** — usable immediately on the Fields build, verifying scroll behavior and reduced-motion fallbacks on a local dev server.
4. **`frontend-design`** — official, no maturity risk, directly counters the generic-aesthetic failure mode from the first line of frontend code.
5. **`orchestrating-gsap-lenis`** — narrow but solves a real, specific bug this exact stack (GSAP + Lenis + Astro) will hit.
6. **`gsap-scrolltrigger` + `threejs-webgl`** — good reference material for the JS-driven layers, used as the plan intends: sparingly, and supplemented (not replaced) by native CSS scroll-timeline and reduced-motion guidance from elsewhere.
7. **`accessibility-auditor`** — directly serves the "minimalist yet informative," reduced-motion-first principles.
8. **`publishing-astro-websites-agentic-skill`** — useful reference for the content-layer architecture; verify against current docs given its low maturity.

Opportunistic, not day-one: `icon-designer` (once real asset production starts), `mcp-builder` (only if an interactive repo-query tool is later wanted), `doc-coauthoring`/`pdf` (for studio documents, unrelated to either build).

---

# Part B — Copyright, trademark & business protection

*Informational research, not legal advice — Claude is not a lawyer, and this section should be treated as a map of the terrain, not a substitute for a licensed IP attorney before any filing, contract signing, or entity formation. Current as of this research pass (August 2026); flagged points are genuinely unsettled and worth re-checking before relying on them.*

## What's protected, and how

Copyright attaches automatically the moment original work is fixed — no registration or notice required. What registration (e.g., with the U.S. Copyright Office) adds isn't protection itself but *enforcement power*: it's a prerequisite to filing an infringement suit for U.S. works, it unlocks statutory damages and attorney's fees (versus having to prove actual financial loss), and it creates a legal presumption of ownership if filed within 5 years of publication. Different studio assets fall into different categories: illustrated art and the logo are straightforwardly protectable visual works; the fictional world and characters get protection for their specific expression, and can get broader "character" protection if they're distinctively enough realized (courts have extended this to settings and species, not just named characters, when the rendering is specific enough — worth knowing given "a Dreamland" is itself a designed setting); website code is registrable as a literary work if it contains genuine creative expression, not pure boilerplate; website copy is registrable as text, and the site as a whole only as a "compilation" if there's real creativity in how it's arranged — each new addition (a new Field, a new Forest recap) is technically a new work for registration purposes, not automatically covered by one filing.

## The AI-assisted art question — directly relevant here

This is the fastest-moving area, and it matters because at least one piece of the studio's own reference art (Seonso's key art) reads as AI-assisted. The U.S. Copyright Office's standing position: copyright protects only human authorship. Its most relevant recent guidance (the January 2025 "Copyrightability" report) draws a specific, practical line — prompting alone, no matter how detailed or iterated, does not establish authorship, because the AI system still determines the specific expressive output. What *does* remain protectable: any human-authored element that stays perceptible in the final piece (a hand-drawn sketch an AI tool then rendered or stylized, if the human-made elements are still recognizable), and a human's selection, arrangement, or sequencing of AI-generated pieces into something new (the way a comic creator's registration protected her arrangement and her own text, while declining to protect the raw AI-generated panels themselves). Registering a mixed piece currently means disclosing the AI involvement and disclaiming the AI-generated portions, claiming only the human-authored expression. The one settled edge is *Thaler v. Perlmutter*: fully autonomous AI output, with no claimed human author, is not copyrightable, and the Supreme Court declined to disturb that. The unsettled edge — exactly how much human creative control over an AI-assisted piece is "enough" — is genuinely open and fact-specific; there's no bright line yet.

**Practical read for Midori Fuwafuwa's asset pipeline:** the strongest protection comes from art built outward from a human sketch, layout, or deliberate compositional choice that AI then helps render — with that human-made backbone still visible — rather than "prompt, accept as-is." Worth keeping that distinction in mind for both the hero brand art and anything the Forest pipeline itself generates or curates, since curated *selection* of real (human-made) assets is a very different, much safer category than generated imagery.

## Trademark: a separate layer

Copyright protects the *work*; trademark protects the *brand identifier* — the studio name, the logo-as-source-identifier, and character names if they're used to sell something (a game title, merch). Trademark rights can arise automatically through actual use in commerce (common-law rights, limited to where the mark is actually used), or through federal registration, which adds nationwide presumption of ownership, a public deterrent record, and the right to use the ® symbol (only after registration — using ® before that is improper; ™ can be used any time to assert an unregistered claim). Current USPTO fees run a flat $350 per class as a base, with total lifecycle cost (filing, maintenance, renewal) commonly landing around $1,000 in government fees alone for a straightforward single-class mark, more with attorney-assisted clearance search and filing. Copyrighting the logo artwork stops someone from copying the *drawing*; it does nothing about a competitor using a different-looking mark that still confuses customers about source — that gap is what trademark closes.

## The two-founder question — probably the highest-leverage item here

Without a written agreement, two people who jointly create a work default to **joint authorship**, generally an equal, undivided interest each, regardless of actual contribution split. The practical risk: under that default, **either founder can independently license, use, or reproduce the shared work without the other's permission** — the only obligation is to share the resulting profit. That means, absent an agreement, one founder could license a character to an outside party while the other disagrees, and the other's only recourse is a cut of the money, not a veto. A basic founders'/IP agreement typically covers: who owns what (individual work vs. jointly created work, and whether that tracks contribution percentage or role), an assignment of both founders' rights into a shared entity if one exists, a requirement for mutual consent before licensing or selling rights (overriding the risky default), what happens to IP and revenue if one founder leaves, how "authorship" is defined for future mixed hand-drawn/AI-assisted work (relevant given Section 2 above), the revenue split itself, and a dispute-resolution mechanism. This is a solvable, one-time, low-cost step relative to the risk it closes.

## The website itself

A visible copyright notice isn't legally required (protection is automatic) but helps rebut an "innocent infringement" defense. A Terms of Use and Privacy Policy are worth treating as necessary rather than optional the moment the site has any backend (the GitHub-API-driven Forest pipeline counts) or any analytics: the current U.S. landscape has around 20 states with active consumer privacy laws, several with low or no minimum-size thresholds, and genuine compliance for a cookie/analytics banner now means actually blocking trackers pending consent, not just displaying a notice. If the site ever accepts user submissions (comments, fan art, a gallery), DMCA safe-harbor protection requires registering a Designated Agent with the Copyright Office ($6, renews every 3 years) — without it, the studio has real exposure for user-submitted infringing content; a pure one-way showcase site doesn't need this yet. On accessibility: there's no finalized federal regulation for *private* business websites (only for government sites, under Title II), but WCAG 2.1/2.2 AA has become the de facto litigation benchmark regardless, lawsuit volume is real and rising (thousands filed annually), and — notably — bolt-on accessibility "overlay" widgets are increasingly viewed as insufficient or even an aggravating factor by courts, versus real code-level fixes. Case Study 01's `prefers-reduced-motion`-first approach actually exceeds the typical AA litigation baseline on motion specifically (that criterion sits at the stricter AAA level) — a genuine head start, though not sufficient by itself for full-site AA conformance.

## Licensing choices to make deliberately

Fonts: confirm whether each typeface used is under an open license like SIL OFL (which explicitly permits commercial use and bundling, with a few conditions on reselling the font itself) or a commercial/proprietary web font license (which often restricts by traffic tier or use-context) — "free for personal use" fonts are a common trap for a commercial site. Any third-party stock assets should be checked for royalty-free vs. rights-managed terms and, specifically, whether the license excludes merchandise/resale use — relevant if characters or art ever go on physical products. If any of the pipeline's own code is open-sourced later, a permissive license (MIT/Apache) lets anyone reuse it freely including competitors, while a copyleft license (GPL/AGPL) requires derivatives to stay open — a business-strategy choice about the *tooling*, entirely separate from and not weakening protection of the *creative IP* itself.

## Business entity — general context, not tax advice

Forming an entity (commonly an LLC for a small creative studio) is generally discussed for two reasons beyond taxes: it separates founders' personal assets from business liabilities, and it gives both founders a single, natural owner to assign their individual and joint IP into — which directly simplifies the joint-authorship risk described above. Tax treatment, formation cost, and ongoing compliance burden vary enough by situation that this is genuinely a "talk to a professional" line item rather than a general one.

## Conclusion — a practical order of operations

None of this needs to happen before building starts, but a few items are cheap now and expensive to fix later — worth sequencing roughly by leverage-per-effort rather than by legal category:

1. **A short founders' agreement between Seonso and Grumpy Carrot's creators, early.** This is the highest-leverage, lowest-cost item on this whole list — it closes the one risk (unilateral licensing under joint-authorship defaults) that actually compounds the longer it's left unwritten.
2. **Be deliberate about which brand art is registered and how, given the AI-assisted question.** For anything going through formal registration, keep track of which pieces have a clear human-authored backbone (worth registering, with AI-generated portions disclaimed) versus pure AI output (not independently protectable) — this doesn't block using AI-assisted art on the site, it just shapes what to rely on for enforcement.
3. **Add a real Terms of Use / Privacy Policy once the Forest pipeline or any analytics goes live**, since a backend pulling GitHub data plus any tracking crosses into the territory current state privacy laws actually regulate.
4. **Check font and asset licenses before shipping**, especially for anything that might end up on merch later.
5. **Trademark registration and formal business-entity formation are reasonable next steps once the studio is operating and the name/mark is stable** — not blockers to building or launching, but worth planning for rather than indefinitely deferring, since both get more valuable (and the trademark clearance search more important) the more the brand is publicly used.

This is the kind of case study that stays genuinely useful over time rather than being a one-time read — worth revisiting as the studio actually starts registering things, signing anything with a third party, or monetizing.

---

## Sources

**Claude Skills**
- [github.com/anthropics/skills](https://github.com/anthropics/skills)
- [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills)
- [freshtechbro/claudedesignskills](https://github.com/freshtechbro/claudedesignskills)
- [alexejluft/brudi — orchestrating-gsap-lenis](https://github.com/alexejluft/brudi/tree/main/skills/orchestrating-gsap-lenis)
- [ComposioHQ/awesome-claude-skills — changelog-generator](https://github.com/ComposioHQ/awesome-claude-skills/blob/master/changelog-generator/SKILL.md)

**Copyright & AI authorship**
- [Copyright in General FAQ — U.S. Copyright Office](https://www.copyright.gov/help/faq/faq-general.html)
- [Copyright and Artificial Intelligence, Part 2: Copyrightability — U.S. Copyright Office](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf)
- [Supreme Court Denies Certiorari in Thaler v. Perlmutter — Reed Smith](https://www.reedsmith.com/our-insights/blogs/viewpoints/102mlpl/supreme-court-denies-certiorari-in-thaler-v-perlmutter-human-only-rule-for-ai/)

**Trademark**
- [Protecting Your Trademark: Basic Facts About Trademarks — USPTO](https://www.uspto.gov/sites/default/files/BasicFacts_1.pdf)
- [Trademark Registration Costs 2026 — Trademark Engine](https://www.trademarkengine.com/blog/how-much-does-trademark-registration-cost/)

**Joint authorship / founders**
- [The Rights of Authors of Joint Works — Johnson Moss Law](https://johnsonmosslaw.com/intellectual-property-blog/the-rights-of-authors-of-joint-works/)
- [Copyright Ownership in Collaborative Projects — Braslow Legal](https://braslowlegal.com/blog/2026/1/16/copyright-ownership-in-collaborative-projects-agreements-and-splits)

**Website compliance**
- [ADA.gov — Title II Web/Mobile Accessibility Rule](https://www.ada.gov/resources/web-rule-first-steps/)
- [Digital Accessibility Under Title III of the ADA — ABA Business Law Today](https://businesslawtoday.org/2025/08/digital-accessibility-under-title-iii-of-the-ada-recent-developments-and-risk-mitigation-best-practices/)
- [DMCA Designated Agent Directory — U.S. Copyright Office](https://www.copyright.gov/dmca-directory/)
- [U.S. State Privacy Laws: 2026 Tracker — Enzuzo](https://www.enzuzo.com/blog/us-state-privacy-laws)

**Licensing**
- [Font FAQ — SIL Language Technology](https://software.sil.org/fonts/faq/)
- [Open Source Licensing for Startups — Promise Legal](https://promise.legal/startup-legal-guide/ip/open-source)

*(Full annotated source lists from both research passes are available in this session's transcript — this file keeps only the primary references.)*
