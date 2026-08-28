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
  integrations: [sitemap()],
});
