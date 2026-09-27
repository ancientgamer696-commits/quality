# Extracted research data — not an approved live catalog

**Collected:** 2026-09-27. Everything below is a dated research snapshot reviewed while planning Quality Glass Emporium. It is **not** current inventory, confirmed pricing, verified testimonials, or permission to reproduce third-party artwork.

## Owner's own website (the shop's previous public site)

| File | Contents |
|---|---|
| `existing-site-pages.csv` | All 51 publicly listed pages: title, heading, word count, lowest ₹ figure seen, source URL, path to its archived text. |
| `raw-pages/*.txt` | Verbatim visible text of each of those 51 pages, with the source URL and capture date in the header. This is the owner's own content, kept for migration. |
| `existing-site-pages-full.json` | Same text plus any JSON-LD structured data found on each page. |
| `existing-site-products.csv` | 32 old-site product cards: slug, description, observed price and crossed-out price, old image path, source URL. Image files were **not** downloaded. |
| `existing-site-categories.csv` | The 10 old-site collections with their taglines. |
| `existing-site-services.csv` | 8 services with English/Hindi names, descriptions and the old "from ₹" starting point. |
| `existing-site-size-guide.csv` | 6 size-to-use-case price anchors (4×6 ₹149 → 24×36 ₹1,999). |
| `existing-site-faq.csv` | The 4 real Q&As from the old Help Center (the fifth card was a "still have questions" banner, not a question). |
| `existing-site-journey.csv` | The old 4-step customer journey. |
| `existing-site-claims-to-verify.csv` | 7 old-site marketing claims (rating, same-day delivery, no hidden charges, 10–200 piece bulk, etc.) that need evidence before reuse. |

`/shop` renders its grid in the browser, so its archived text is empty by design — the product cards were captured from the rendered grid instead (see `existing-site-products.csv`).

## Competitors (feature and policy benchmarking only)

| File | Contents |
|---|---|
| `competitor-observations.csv` | Curated flow, option and price observations from the six reviewed sites. |
| `competitor-pages-extract.csv` | 13 reviewed competitor pages: which page, transport/turnaround wording found, shipping-charge wording, payment methods, size handling, upload limits, ₹ and $ figures seen, and **one short quoted snippet** so a claim can be traced back. |
| `competitor-policies.csv` | Side-by-side shipping, replacement-window, upload/custom-size and payment-method comparison, plus what is worth copying and what to avoid. |

No competitor images, artwork, page copies or customer reviews were archived. Snippets are kept to roughly one line each for attribution; nothing from a competitor page is marked for reuse on the new site.

## Platform and requirements

| File | Contents |
|---|---|
| `shop-profile.json` | Public shop identity: name, address, phone, hours, rating snapshot — each with a `owner_confirmed: false` style flag. No UPI ID or QR was invented or imported. |
| `feature-requirements.json` | Requested collections, marketing sections, payment/proof workflow, manager modules and the selected free-tier stack. Requirements, not shipped features. |
| `platform-limits.csv` | Free-tier arithmetic with official documentation URLs and caveats. |

| `ALL-EXTRACTED-DATA.md` | Single-file bundle: every table above plus the verbatim text of all 51 archived pages. Rebuild with `build_single_file_bundle.py`. |

## Rebuild scripts

`extract_public_data.py` (old-site cards and categories), `extract_owner_site_pages.py` (crawls the old site's sitemap, skipping robots.txt-disallowed paths), `extract_owner_structured.py` (no network; parses the archived text), `extract_competitor_pages.py` (structured competitor facts only), `build_single_file_bundle.py` (regenerates the single-file bundle). Run them only when you deliberately want to refresh this research.

**Not included:** competitor images, scraped reviews, protected pages, guessed WhatsApp/UPI credentials, any API tokens, bank details or customer payment evidence. A verified merchant UPI ID/QR was never found or supplied, so none is recorded here.

The longer analysis and design work sits in [`../research/`](../research/); the prototypes are in [`../demos/`](../demos/).
