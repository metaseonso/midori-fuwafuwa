// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
// Stage A: served from GitHub Pages at a project-site subpath.
// Stage B swaps `site` to the custom domain and drops `base` once that's live.
export default defineConfig({
  output: 'static',
  // Every field is fetched the moment its link is on screen, so stepping into
  // a dream is instant rather than a page load. The three field pages are a
  // few KB of HTML each and the art is already in the browser's cache from
  // the sky, so this costs almost nothing and removes the wait entirely.
  prefetch: {
    prefetchAll: true,
    defaultStrategy: 'viewport',
  },
  site: 'https://metaseonso.github.io',
  base: '/midori-fuwafuwa',
  vite: {
    build: {
      // Lightning CSS (the default) merges
      //     animation: plane-part linear both;
      //     animation-timeline: scroll(root);
      // into `animation: linear both plane-part scroll(root)` — and
      // animation-timeline is NOT a component of the animation shorthand, so
      // browsers reject that declaration outright and the animation-name
      // resolves to none. Every scroll-driven animation on the site was dead
      // in the built output while working perfectly in dev, which is why it
      // only ever showed up on the deployed page. esbuild's CSS minifier does
      // not perform that merge.
      cssMinify: 'esbuild',
    },
  },
  integrations: [sitemap()],
});
