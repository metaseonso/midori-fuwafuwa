// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
// Stage A: served from GitHub Pages at a project-site subpath.
// Stage B swaps `site` to the custom domain and drops `base` once that's live.
export default defineConfig({
  output: 'static',
  site: 'https://metaseonso.github.io',
  base: '/midori-fuwafuwa',
  integrations: [sitemap()],
});
