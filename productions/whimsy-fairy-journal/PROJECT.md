---
title: "Whimsy (working title) — the fairy journal"
studio: Midori Fuwafuwa Studio
status: intake — concept stage
date_added: 2026-08-19
folder_name: provisional — rename once the real title is set
---

# Whimsy (working title) — the fairy journal

## What it is
A product, not a book. A magical fairy keeps your diary entries, journal pages, daily
planner agendas, scrapbooks, pinboards, notes, and doodles safe — then sprinkles fairy dust
to turn them into a whimsical world you can explore.

Mundane tasks, to-do lists, random ideas, and doodles come alive with vivid images and
charming animations. **As the seasons change, you receive personalised recaps of your own
storyline**, woven together with fascinating facts ranging from the earth to the stars and
everything in between.

## Voice (founders' own words — keep)
> They say not to get lost in your fantasies, but we know you're a secret genius with a
> method to your madness.
>
> So we say: don't get lost in your fantasies — let's FIND ourselves THROUGH them!
>
> With just a bit of WHIMSY! 😉🧚‍♀️👼😊

That last line is doing real work. The pitch reframes "lost in fantasy" as a strength rather
than a flaw, which is the emotional core of the product and should survive into the final
copy.

## The fairy
A new character — not Seonso, not Grumpy Carrot, not the studio's mint cloud mascot. She is
this production's own mascot and guide.

From the reference image: pastel lavender/lilac hair with flowers worked into it, large
translucent iridescent wings, a soft pastel green-and-pink dress, hovering in a trail of
gold sparkles. Small, cheerful, chibi-adjacent proportions with large eyes.

## Reference art
Current file: `reference/` — **temporary placeholder, described by the founders as "apt."**
Direction reference, not a model sheet.

What it establishes:
- An open journal/book as the literal ground plane — the world grows *out of* the page.
- **Floating islands** above the pages, each carrying a tiny structure (a domed gazebo or
  pavilion), grass, and small plants. Several at varying scales and depths.
- Gold fairy-dust trails and sparkle motes connecting the islands.
- Real handwritten text visible on the book pages underneath.
- A fountain pen resting on the book. Soft warm light, shallow depth of field.
- Rendered/CGI storybook style — glossy, dimensional, soft-focus.

## The structural finding — this is the Forest engine, pointed somewhere new

**This production and the studio's own website research describe the same machine.**

Case Study 02 designed a "Forest": a five-stage pipeline that reads real activity on a clock
(monthly + seasonal), uses an LLM to build a **narrative arc** from it, **selects and
sequences real committed assets** to illustrate that arc, and renders the result as a
data-driven scroll journey where the template is fixed and only the data changes.

This product is that same pipeline with the input swapped:

| Stage | Studio Forest | Whimsy |
|---|---|---|
| Input | GitHub commits, PRs, changed art files | Diary entries, notes, planners, doodles |
| Clock | Monthly + seasonal | Seasonal ("as the seasons change") |
| Synthesis | Story arc from a period of work | Personalised storyline from a period of life |
| Illustration | Real committed production art | The user's own doodles + generated imagery |
| Output | A forest that thickens over time | A whimsical world to explore |

Case Study 02's central conclusion was that **everything in that pipeline is off-the-shelf
except one thing**: narrative-arc construction and story-relevant asset curation. No existing
tool does either.

That one custom piece is now the core engine of a saleable product, not just a nice touch on
the studio's own site.

**Consequences worth acting on:**

1. **The studio's Forest is a working prototype of this product.** Building it against the
   founders' own GitHub repos is the cheapest possible way to develop and de-risk the engine
   — real data, no users, no privacy exposure, no support burden.
2. **The narrative-arc skill is product R&D, not site polish.** It was already ranked the
   highest-value thing to build. This doubles that: it now has two uses.
3. **Build the Forest before the product.** Same engine, far lower stakes. Whatever the
   narrative voice gets wrong on a quiet month, it gets wrong on a quiet month of someone's
   diary too — better to find that out on your own data.
4. **The "fascinating facts" layer is genuinely new** and has no Forest equivalent. Weaving
   external knowledge (earth to stars) into a personal storyline is a second custom piece,
   separate from arc construction. Worth scoping on its own.

## Flags — read before any build

### Privacy is the defining constraint of this product
The studio Forest reads *public* GitHub repos. This product reads **private diaries** — among
the most sensitive personal data that exists. That is a categorically different obligation,
not a scaled-up version of the same one.

Case Study 03's privacy section moves from an eventual to-do to a day-one design constraint:
around 20 US states have active consumer privacy laws, several with low or no minimum-size
thresholds. Beyond compliance, sending private journal content to an LLM API needs a
deliberate, stated, and honoured data policy — what leaves the device, what is retained,
what trains anything. Trust is the product here; a single mishandling would be terminal.

Worth deciding early whether synthesis runs locally, in a private cloud, or via a
zero-retention API arrangement. That choice constrains the architecture, so it cannot be
deferred to the end.

### Likely to attract minors
"Diary," "doodles," and a fairy guide will draw young users regardless of who the product is
aimed at. If under-13s are in scope, COPPA applies in the US and adds real obligations
(verifiable parental consent, restrictions on data collection). Deciding the intended age
range early is cheaper than retrofitting compliance. Worth confirming as an explicit product
decision, not letting it be settled by whoever shows up.

### Art-style tension with Production 01
The Kits' reference is soft 2D watercolour. This reference is glossy 3D-rendered CGI. The
studio's stated value principles include *"assets simple to produce, in one consistent design
language."* The website research allows each Field its own palette accent and mascot pose —
variation *within* a style, not two different rendering pipelines.

Two productions in two different visual languages needs a deliberate call:
- **Option A** — one house style (likely the 2D/chibi register, which the research also found
  is the cheapest to render well) with each production differentiated by palette and motif.
- **Option B** — each production keeps its own native style, and the site's job is to hold
  both gracefully.

Option A is cheaper to produce and closer to the stated principles. Option B is truer to each
production's own feel. Not urgent today, but it should be decided before real asset production
starts on either.

## Product decisions — confirmed 2026-08-19

**Audience: non-tech-savvy people.** This is the defining product constraint, and it settles
the interaction model.

**Interaction model: an AI you just message.** The user talks to it in plain language and it
does the organising. No folder trees, no tagging UI, no setup. The fairy *is* the interface.

That is unusually well matched to the audience. A conversational surface has no learning curve
— the user already knows how to send a message. It also fits the engine: unstructured personal
input is exactly what an LLM handles well, and rigid forms are what non-technical users abandon.

**Age floor: 13+.** Deliberately set to stay out of COPPA. Stated in terms, no knowing
collection from under-13s. If genuine demand appears from younger users, revisit then with a
parental-consent flow — not before. Rationale from the founders: keep compliance burden low so
the studio's energy stays on making things.

**Platform: undecided — app vs. Telegram vs. something else.** Flagged by the founders as a good
question and handed to research. See "Open research task" below.

## Open research task — platform and go-to-market

Requested by the founders: what the market is primed for, and what scales best.

Needs to cover:
- **Telegram/WhatsApp bot vs. native app vs. web app** for a conversational AI product aimed at
  non-technical users — adoption friction, discovery, retention, and platform risk (building on
  someone else's messaging platform is cheap to start and precarious to depend on).
- **Existing competitors** in AI journaling / conversational memory-keeping, and where the gap is.
- **Cost per user** of running seasonal LLM synthesis, and what pricing that implies.
- **Distribution** — how a two-person studio actually reaches non-technical users, which is a
  very different problem from reaching a technical audience.
- **Privacy architecture options** and their cost, since this constrains the platform choice.

## Still needed
- **The real product name.** "WHIMSY" and "FIND" are both capitalised in the pitch; the founders'
  own file was named `WhimsyDraft`, so "Whimsy" is treated as the working title. Confirm.
- The fairy's name.
- Whether "personalised recaps" are private-only or shareable.
- Privacy architecture decision (local / private cloud / zero-retention API).

## Intake log
- 2026-08-19: Production created. Concept, pitch voice, and fairy reference recorded. Identified
  as sharing the Forest pipeline architecture from `research/case-study-02-living-pipeline.md`.
