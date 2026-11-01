# Link previews (Open Graph) — how it works here

`python3 scripts/build.py shop` produces the full OG set automatically:

- **Site card** — `index.html` head gets `og:*` + `twitter:*` tags + `og-cover.jpg` (1200×630).
- **Product cards** — every SKU gets `/share/<slug>/` with its own title, price line and
  the matching artwork (`/og/<art>.jpg`, extracted from the inlined data-URIs at build time).
  Share `quality-glass.pages.dev/share/sacred-lotus/` on WhatsApp → rich card → tap opens the shop.
- **Category cards** — `/share/c-religious/` etc.
- Override the absolute URLs at build time with `QGE_ORIGIN=https://your-domain` when you move
  off the pages.dev preview.

After deploying, warm/verify the crawlers:
1. https://developers.facebook.com/tools/debug/ → paste the URL → **Scrape Again** (this also
   refreshes WhatsApp's cache, which it shares).
2. Send the link to yourself on WhatsApp — expect title + image + description.

Stale previews on your phone = WhatsApp's CDN cache; re-scrape + resend, or append `?v=2`.
