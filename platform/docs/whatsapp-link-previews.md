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

## Live copies

| Domain | What it serves | How updated |
|---|---|---|
| `https://ancientgamer696-commits.github.io/quality/` | full OG build (github.io-baked URLs) | `git push` to `gh-pages` branch (see below) |
| `https://quality-glass.pages.dev/` | official domain — needs one zip upload | upload `platform/quality-glass-shop-pages-upload.zip` in CF Pages dashboard |

Re-render branded cards after catalog edits: `python3 scripts/make_og_cards.py` (needs Pillow +
repo fonts). Then rebuild + push both:
```
python3 scripts/build.py shop                     # pages.dev variant -> repo zip
QGE_ORIGIN=https://ancientgamer696-commits.github.io/quality python3 scripts/build.py shop
# copy apps/shop/dist/* into a clone of the gh-pages branch and push
```
Product share links: `…/share/sacred-lotus/`, categories `…/share/c-religious/` — each card shows
that item's own 1200×630 art with name + price, tap-through to the shop.

Manager app: run `python3 scripts/build.py manager` — OG brand card + icons are injected there too.
If the manager lives on its own domain, build with `QGE_MGR_ORIGIN=https://that-domain`.
