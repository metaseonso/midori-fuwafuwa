import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

// Reads productions/<slug>/recaps/*.json directly from the studio's own
// productions folder — not duplicated into src/content. Fixture data only
// in Stage A; the real pipeline swaps the source, not this schema.
const recaps = defineCollection({
  loader: glob({ pattern: "*/recaps/*.json", base: "../productions" }),
  schema: z.object({
    type: z.enum(["sapling", "grove"]),
    period: z.string(),
    title: z.string(),
    season: z.enum(["spring", "summer", "autumn", "winter"]),
    summary: z.string(),
    scenes: z.array(
      z.object({
        prose: z.string(),
        mood: z.string(),
        sourceLabel: z.string(),
        sourceHref: z.string(),
        asset: z.object({
          kind: z.enum(["sprout", "leaf", "bud", "blossom", "branch"]),
          alt: z.string(),
        }),
      })
    ),
  }),
});

export const collections = { recaps };
