// Prepends the configured base path (astro.config.mjs `base`) to a
// root-relative path. Needed because Astro does not rewrite hardcoded
// string hrefs/srcs itself — only its own asset pipeline gets that for
// free. Stage A serves from a GitHub Pages subpath; Stage B drops `base`
// entirely for the custom domain, and this becomes a no-op everywhere it's
// used, so nothing else has to change when that happens.
export function withBase(path: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, "");
  return `${base}${path}`;
}
