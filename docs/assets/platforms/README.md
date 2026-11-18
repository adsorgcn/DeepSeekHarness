# Platform icons

24 icons from Simple Icons **16.38.0**, fetched from the official npm package.

- `platforms.svg`: transparent SVG sprite with `p-<slug>` symbol IDs, original 24 × 24 viewBoxes, and glyph color inherited through `currentColor`.
- `sources.json`: exact slugs, fixed-release SVG URLs, upstream brand sources, original hashes, brand colors, and per-icon license metadata where supplied.
- `SIMPLE-ICONS-LICENSE.md` and `SIMPLE-ICONS-DISCLAIMER.md` are copied unmodified from that release. The package is CC0-1.0; brand-specific license information and trademarks are separate, as documented upstream.

Example (set the surrounding SVG's color to white for a white glyph):

```html
<svg viewBox="0 0 24 24" aria-hidden="true" style="color:#fff">
  <use href="assets/platforms/platforms.svg#p-wechat"></use>
</svg>
```

Original paths and proportions were preserved. These assets identify platforms; they do not imply affiliation or endorsement. No Aside imagery or code is included. Standalone duplicates are intentionally omitted.
