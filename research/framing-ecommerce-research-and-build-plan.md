# Custom framing business — competitor research and complete build blueprint

**Research date:** 27 September 2026 (India). **Market:** India-first, with Lucknow/UP local operations as a sensible initial service area. **Deliverable scope:** Two independently deployed websites (customer storefront + private manager panel), one shared backend API, data model, operational workflows, and rollout plan. This is a review of publicly visible pages, **not** an authenticated checkout test, full site crawl, or permission to reuse competitors' text/images.

> **Executive recommendation:** Start with Cloudflare Pages (two sites) + one Cloudflare Worker API + D1 + private image storage. Build a focused **Upload → Preview → Customize → Upfront price → Checkout** experience. Make the manager panel a production/fulfilment tool, not merely a product editor. Launch a small, curated catalog rather than copying every competitor category. Add a VPS only when measured workload or special processing requires it.

## 1. What the six websites actually offer

Observed prices are **public snapshots**, not guaranteed current quotes. A “from” price can change with size, finishes, quantity, shipping, tax and promotions. Different materials/products are **not** directly price-comparable. All prices below were visible on the linked pages at research time.

| Site | Observed positioning and useful public data | Feature to learn from | Your opportunity |
|---|---|---|---|
| [OnlineFraming](https://onlineframing.in/) | Very broad catalog: synthetic/metal/wood, gallery walls, gifts, certificates, canvas, mirrors, unusual objects. “Upload & Frame” takes visitors to a separate [SimulArt-powered upload page](https://framing.onlineframing.in/bridge.php); public page accepts JPG/TIF/PNG/GIF/PDF/WEBP up to a stated 64 MB/400 MP. Site advertises pan-India free shipping. | Breadth, occasion-led browsing, custom art framing. | Keep upload/configure/cart on **one brand-consistent flow**; do not launch with an overwhelming mega-menu. |
| [Framebazaar](https://framebazaar.com/) | Premium framing/printing. [Osaka metal frame](https://framebazaar.com/products/osaka-frame) displayed **from ₹2,499**; selectable sizes/colors, photo upload up to a stated 50 MB, preview, estimated fulfilment/delivery dates, WhatsApp custom-size link. [The Tabletop](https://framebazaar.com/products/the-tabletop) displayed ₹1,499 sale / ₹1,999 regular, with stated print/frame sizes and material inclusions. | Material transparency, product presentation, preview, ETA and bespoke enquiry. | Show exact **photo opening vs outer dimensions**, local delivery expectation, and a simpler decision path. |
| [Framebridge](https://www.framebridge.com/pages/what-are-you-framing) | US premium custom framing; routes by **digital upload, physical art, documents, 3D objects, textiles**. [Pricing](https://www.framebridge.com/pages/pricing) shows digital sizes from **$70** (up to 5×7 in) and physical pieces from **$85**, with higher size bands and add-ons. | A guided “What are you framing?” intake, material education, transparent band pricing. | India-specific, faster and lower-friction mobile UX; offer mail-in/art intake **only after** logistics/insurance are designed. USD figures are not India price benchmarks. |
| [CanvasChamp framed prints](https://www.canvaschamp.in/framed-prints) | Page displays **starts ₹523** (tax-inclusive), custom width/height choices shown from 8–40 in, many styles, matte/gloss paper and no/white/black mat choices; discusses cropping and correction. | Range of configuration options and artwork guidance. | Use curated “good / better / premium” choices, live image-resolution warnings and a continuously updated price. |
| [Framing World](https://framingworld.in/) | Premium artwork/archival-print positioning; site shows fine-art prints, UV printing, acrylic, canvas etc. Its [metal-frame product](https://framingworld.in/collections/fine-art-prints/products/metal-frame) displayed **from ₹1,450** and variants for finish, glazing (normal/museum glass, acrylic/museum acrylic) and paper (studio or archival). | Premium material tiers and preservation details. | Explain who needs premium glazing/paper; avoid huge unmanageable variant combinations in the UI. |
| [VistaPrint photo with frame](https://www.vistaprint.in/photo-gifts/photo-with-frame) | Product page displayed **₹310 for 1 unit** (base configuration), size/color choices, templates or upload, volume-price guide (e.g. 5 of same design shown as ₹1,250), pincode delivery estimate. States ready-to-hang assembly and limited same-day Mumbai service. | Simple purchase path, clear quantity breaks, pincode ETA. | Make pincode eligibility and exact shipping fee visible before the last checkout step; provide a stronger framing-specific preview. |

**Research limitations:** Framebridge’s interactive designer and some embedded components were not fully observable in a text-page inspection; some products require interaction to reveal the actual combination price. No claim here about competitor conversion rates, backend architecture, actual delivery reliability, or every item in their catalogs. Do **not** scrape/rehost product photos, copied descriptions or customer reviews; create your own assets and copy. This is an **evidence-based feature benchmark**, not a bulk export of their databases.

### Practical competitive thesis

Positioning: **“Beautiful custom frames without guessing: preview the result, know the print quality and total price, and track every step.”** Differentiate on (1) guided customizer; (2) transparent material and dimensions; (3) WhatsApp-assisted custom enquiries with logged quotations; (4) mobile performance in India; (5) trustworthy local production/dispatch updates; (6) an owner-facing operational system. Do not claim “fastest,” “museum grade,” or “free shipping” unless the product/process supports it.

## 2. What to sell first

**Launch catalog (MVP):** (A) upload-and-frame photo prints; (B) ready-made empty photo frames; (C) tabletop/gift frames; (D) certificate/artwork framing **quote request**. Offer 4–6 mouldings (e.g. black/white/natural/gold), 5–8 standard sizes, matte/gloss print, none/white/black mat, acrylic as default glazing, wall/tabletop hardware only where compatible. Each option needs a real supplier SKU, cost, lead time and availability.

**Next:** gallery walls, collage templates, premium solid wood, archival paper, higher-grade acrylic, custom dimensions, B2B volume pricing. **Later only with production validation:** mail-in original art, textiles/jerseys/shadow boxes, glass shipping, mirrors, acrylic UV printing, AI restoration. Avoid promising custom 40×40 in frames until packaging, courier and damage rates are tested.

**Customer journey:** Home → choose “Upload a photo” / “Shop a frame” / “Frame physical art” → product/configurator → review dimensions/crop/resolution/price → cart → address + pincode + shipping → payment → order confirmation → tracked production/delivery + support/replacement. Guest checkout must work; Google sign-in is optional convenience, never a purchase blocker.

## 3. System architecture: two websites, one API

```text
shop.yourdomain.in (Cloudflare Pages)       manager.yourdomain.in (Cloudflare Pages)
  public catalog + customizer + checkout        private RBAC dashboard + fulfilment
                  \                              /
                   \  HTTPS /api/...            /
                    api.yourdomain.in (Cloudflare Worker)
                      |       |          |         |
                   D1 SQL   object     payments   Delhivery
                   metadata storage    webhook    integration
                          private originals; public product thumbnails
```

**Repo:** one TypeScript monorepo: `apps/shop` (React + Vite; prerender/SSR strategy for SEO), `apps/manager` (React + Vite), `apps/api` (Hono Worker), `packages/shared` (types + Zod validators), `packages/pricing` (pure price calculation), `db/migrations`, `docs`. Cloudflare Pages has separate deployments/build targets. An API route at `api.yourdomain.in` avoids messy cross-origin setup; allow only both known domains in CORS, or use a same-origin proxy with secure cookies if chosen. Backend alone owns prices, inventory, order transitions and permissions. **No secrets in Pages bundles.**

**SEO decision:** Do not ship a JavaScript-only public catalog and hope for search traffic. Prerender home/category/product/FAQ/occasion pages at build time and refresh after catalog changes, or adopt an edge-SSR framework if genuinely needed. Manager remains a normal private SPA with `noindex` and authentication. Use semantic HTML, canonical URLs, sitemap, Product structured data only for real published products, OG images, accessibility and mobile-first images. PWA is optional enhancement, not a prerequisite.

**Storage choice:** Use **one** canonical asset store. Easiest Worker-integrated choice is Cloudflare R2 **if you can enable its subscription/payment setup**; otherwise use private B2 with a tested signed-upload/serve design. Use ImageKit **as a delivery/transform layer**, not as an unplanned second source of truth. Keep customer originals private, put only safe product thumbnails behind a public CDN; never expose B2 keys, payment screenshots, original private photos, or unrestricted buckets. B2+ImageKit origin configuration and transformation limits must be tested before committing. Original uploads get opaque IDs, size/MIME validation, antivirus/unsafe-content strategy if accepting arbitrary PDFs, EXIF orientation processing and retention/deletion rules. For MVP accept JPG/PNG/WEBP only; add PDF/TIFF after handling is proven.

**Why not Oracle on day one?** You proposed Workers+D1 and Oracle VPS together; they are alternatives for the primary API/database, not components to run in parallel without need. A VPS adds patching, backups, firewall, observability and single-machine availability risks. Use it later for image rendering/print-prep, long-running jobs or heavier relational workloads. **Do not use fake cron jobs to evade idle-resource reclamation.** If moved later, run Node/Fastify or Django + Postgres on a monitored VPS, with proper backups and a staging migration; do not assume D1 schema/SQL and Postgres are drop-in compatible.

## 4. Verify the proposed free-stack assumptions

| Component | Verified planning assumption / caveat |
|---|---|
| Cloudflare Pages | Free tier documentation lists **500 builds/month**, **100 projects/account**, up to **20,000 files/site** and one concurrent build. Not “unlimited sites.” Static delivery and dynamic Worker/API usage have different limits. [1](https://developers.cloudflare.com/pages/platform/limits/) |
| Cloudflare Workers | Free: **100,000 requests/day** and **10 ms CPU per invocation**, 128 MB memory; quota overflow can return Error 1027. Keep image transformation and slow jobs off synchronous free Worker requests. Pages Functions, if used, share Workers quotas. [2](https://developers.cloudflare.com/workers/platform/limits/) |
| Cloudflare D1 | Free billing allowance: **5M rows read/day**, **100K rows written/day**, **5 GB aggregate storage**; importantly **500 MB max per database on Free** (10 free DBs listed). Those are *rows*, not “queries/visits.” Keep photos out of D1; index queries and test realistic read counts. [1](https://developers.cloudflare.com/d1/platform/pricing/) [1](https://developers.cloudflare.com/d1/platform/limits/) |
| Backblaze B2 | Current pricing page says **first 10 GB storage free**, free egress up to **3× monthly average stored volume**, and partner CDN paths including Cloudflare can have free egress. **“1 GB/day” is an outdated rule of thumb**; B2→ImageKit is not automatically the same as B2→Cloudflare. Test exact routing, account setup and billing. [1](https://www.backblaze.com/cloud-storage/pricing) |
| ImageKit | Current plan page lists free **20 GB/month bandwidth** and **3 GB fixed DAM storage**, plus plan-specific transformation/feature limits. 20 GB/mo is **not unlimited traffic**. [1](https://imagekit.io/plans/) |
| Cloudflare R2 (alternative) | Standard-class free allowance **10 GB-month**, **1M Class A** and **10M Class B operations/month**, egress free; requires enabling an R2 subscription/checkout, so do not assume “no card.” Set billing alerts. [1](https://developers.cloudflare.com/r2/pricing/) [2](https://developers.cloudflare.com/r2/get-started/) |
| Oracle Always Free (optional) | **Current** docs say Ampere A1 free equivalence **2 OCPUs/12 GB RAM**, and **200 GB total block volumes**; old 4/24 marketing is outdated. Idle instances may be reclaimed, allocation depends on region/capacity. Home region choice and payment verification need checking. [1](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) |
| Google Maps | The official Maps Embed API is no-charge but requires **API key and billing enabled**; simplest no-billing fallback is a normal “Open in Google Maps” location link. [2](https://developers.google.com/maps/documentation/embed/quickstart) |
| Payments / courier | wa.me deep links have no WhatsApp Business API charge but **do not** automatically capture, verify or fulfil orders. Payment gateways charge transaction fees; a current Razorpay article describes a standard domestic **2% platform fee + GST**, subject to merchant agreement. Delhivery supplies authenticated API functions for serviceability, shipment creation, labels and tracking, with real shipping charges. [3](https://razorpay.com/blog/upi-charges-explained-mdr-vs-platform-fees/) [1](https://help.delhivery.com/docs/client-developer-portal-1) |

**₹0 is not a complete business budget:** domains, gateway fees, delivery, packaging/breakage, SMS/email/WhatsApp API if added, production labour, taxes, extra storage and paid upgrades still cost money. Check current provider terms, billing setup and regional account availability before launch.

## 5. Customer website: page-by-page specification

**Home:** Clear hero with primary “Upload & Frame,” category shortcuts, 3-step explainer, honest starting price, material comparison, real customer photos with consent, FAQ, delivery/pincode teaser, local story and contact.

**Catalog and search:** Categories by customer intent (photo framing, empty frames, gifts, certificates), not 100 microcategories. Filter by price, finish, material, size, orientation, use case; sort, breadcrumbs, in-stock flags and accurate product cards.

**Product page / configurator:** Sticky photo preview + sticky total price on mobile. Step 1 upload or choose no print; step 2 size/orientation, show image opening and outer frame dimensions; step 3 moulding/color; step 4 paper/mat/glazing/hardware; step 5 crop/zoom/rotate and explicit preview approval. Show original resolution, required pixels for chosen printed dimensions (`width_inches × target_ppi`, likewise height; e.g. 8×10 at 200 PPI ≈ 1600×2000 px), potential blur warning (not an automatic rejection), safe margin/bleed where relevant, quantity, manufacturing time and shipping estimate. **Preview is illustrative**, not proof of color accuracy. Persist configuration draft securely across refresh.

**Cart/checkout:** Editable line items, coupon, exact tax/shipping and grand total, address, pincode validation, delivery promise, privacy/return policy, optional guest checkout and optional verified Google login. Require customer approval of crop, dimension and custom-item replacement terms. Payment success must come from verified gateway webhook/server reconciliation, **never** a browser redirect alone. Manual UPI may be available initially: show dynamic order reference, collect transaction ID or screenshot, mark `payment_pending_verification`; do **not** mark paid or ship based solely on screenshot. COD only where serviceable and operationally acceptable. WhatsApp order link opens a conversation, not a confirmed order/payment.

**Account/tracking:** Order timeline with real statuses, tracking URL, invoice, support/replacement claim, re-order, photo deletion request. Public tracking lookup must use a sufficiently random token or authenticated account, not enumerable order numbers.

**Content:** About, contact, FAQ, materials, print-resolution guide, shipping/pincode policy, custom-item cancellation/replacement policy, privacy policy, terms, corporate enquiry and optional pickup-store map link.

## 6. Manager website: operational modules and roles

| Module | Required functions |
|---|---|
| Dashboard | Paid orders needing approval, overdue production, dispatch due today, unpaid manual payments, low material stock, recent returns/claims, sales net of discounts/refunds. |
| Orders | Search/filter; inspect approved crop/photo under authorization; flags for low resolution; assign job; audit each status; download print-ready work order; manual hold/approval; add tracking; refund/replacement request. |
| Production board | `new → artwork_check → awaiting_customer_approval → print → frame_assembly → quality_check → packed → shipped → delivered` with exceptions `on_hold / cancelled / remake / returned`. Record user, time, reason and photo evidence when needed. |
| Catalog + pricing | Categories/products, option compatibility, visual assets, draft/publish, per-size price rules, tax class, lead time, bulk-pricing tiers, coupon validity and preview-before-publish. |
| Inventory / purchase | Track moulding **length**, paper sheets/area, acrylic sheets/area, hardware units, finished-goods SKU, reorder thresholds, purchase receipts, waste/cut allowance. Reserve on paid order; release on cancellation; reconcile periodically. |
| Customers + CRM | Order history, addresses, consent status, support tickets, WhatsApp conversation link, custom-quote pipeline (do not store unrestricted private chat unless consented). |
| Payments, bills, khata | Payment method/reference/webhook status, pending verification queue, refunds, invoices/credit notes; separate **supplier ledger or customer credit ledger** with double-sided entries and approval. Never edit balances directly; append adjustment entries with reason. Get accountant review for GST/invoice requirements. |
| Shipping | Serviceability, package dimensions/weight, shipping cost, label/waybill, pickup request, tracking sync, NDR/return-to-origin exceptions and damage claims. |
| People/settings | Owner/staff accounts, RBAC, optional 2FA for owner, audit log, tax/shipping rules, notification templates, backup/export, privacy retention controls. |

**Roles:** Owner = everything + financial settings; Manager = fulfillment/catalog, limited financial views; Designer = assigned artwork jobs; Production = assigned workshop tasks; Support = customer orders/tickets, no private payment credentials. Role checks happen on every API endpoint; a hidden nav item is not security. Google sign-in proves identity **only**; grant staff roles from a server-side owner-controlled allowlist. Require HTTPS, HttpOnly Secure SameSite session cookies or equivalent short-lived session design, CSRF protection where cookie auth is used, short-lived signed URLs to private assets, and audit logs. Google sign-in production branding may require verification; request minimal profile/email scopes. [3](https://developers.google.com/identity/verification/authentication-policy-compliance)

## 7. Backend: data, contracts and invariants

**Core D1 entities** (UUID/ULID keys, created/updated timestamps, integer paise not float money):

- `users`, `identities`, `sessions`, `staff_roles`, `addresses`, `consents`.
- `categories`, `products`, `product_media`, `mouldings`, `materials`, `sizes`, `option_compatibility`, `price_rules`, `price_rule_versions`.
- `asset_uploads` (`owner_id`, object_key, MIME, bytes, pixel_width/height, status, expiry, deleted_at); keep raw binary in object storage.
- `carts`, `cart_items` (immutable chosen options + preview/crop reference), `quotes`, `quote_items`, `quote_expiry`.
- `orders`, `order_items` (immutable **price and option snapshot**, asset references), `order_status_events`, `job_tasks`, `quality_checks`.
- `payment_attempts`, `payment_events` (unique gateway event ID), `refunds`, `invoices`, `tax_lines`.
- `stock_items`, `stock_movements`, `stock_reservations`, `purchase_orders`, `supplier_ledger_entries`.
- `shipments`, `tracking_events`, `coupons`, `coupon_redemptions`, `reviews`, `support_tickets`, `audit_logs`, `settings`.

**Price service:** One shared pure calculator, server authoritative. Example (illustrative formula, **not market pricing**): `base moulding cost by perimeter + print cost by area + glazing + mat + backing/hardware + labor + packaging + waste + margin + shipping + applicable tax − eligible discount`. For matting, calculate **outer** dimensions from artwork opening, mat width and moulding width; charge on outer footprint. Round in integer paise, then produce an itemized tax-inclusive/exclusive breakdown according to accountant-approved settings. Version rules and store accepted price snapshots. `/api/quotes` computes and signs a short-lived quote; checkout recomputes, checks availability and returns a price-change prompt if necessary.

**Inventory invariants:** Reserve after payment confirmation (or reserve briefly during checkout if capacity demands it); prevent negative sellable stock using conditional update/transaction where possible. Have an owner-approved backorder override. For custom frames, BOM consumption happens against dimensions and supplier stock, not simply `product.quantity -= 1`. Every adjustment records event ID and actor.

**Minimum API surface (JSON, `/api/v1`):**

| Public/Customer | Protected manager/webhook |
|---|---|
| `GET /catalog`, `GET /products/:slug`, `POST /quotes`, `POST /uploads/init`, `POST /uploads/complete`, `POST /checkout`, `GET /orders/:token`, `POST /auth/google/callback` | `GET/PATCH /admin/orders`, `POST /admin/orders/:id/transition`, CRUD `/admin/products`, `/admin/price-rules`, `/admin/inventory/movements`, `/admin/shipping`, `/admin/payments/manual-verify`, `POST /webhooks/payment`, `POST /webhooks/shipping` |

**Transaction flow:** Verify item assets/quote/price/pincode → idempotently create pending order + payment attempt (server-side) → process signed payment webhook and independently verify captured amount/currency/order → idempotently mark paid, write event and reserve stock → create production job → QC → book shipment → emit customer updates. For webhook retries, enforce unique event IDs and idempotency keys; use DB transactions/batches where appropriate. Never trust client-sent role, discount amount, shipping price or order state.

**Uploads:** Give each user/order isolated object keys, short-lived signed upload authorization where supported; enforce type/size and quotas before issuing upload; private originals and short-lived display URLs. Retain source photo only as long as stated in privacy policy or needed for remakes; offer deletion schedule and access logging. B2/R2 exact upload mechanism and image pipeline should be prototyped early; avoid passing 50–100 MB images through a Worker needlessly.

**Operations:** Separate dev/staging/prod bindings; schema migrations in CI; daily exports + restore drill; use D1 Time Travel as recovery assistance, **not your only backup**. Free D1 currently lists a 7-day Time Travel window. Logs/alerts for failed webhook, zero-order spikes, stock mismatch, slow queries, storage growth and costs. Rate-limit auth, quoting, upload init, coupon attempts and tracking lookup. [1](https://developers.cloudflare.com/d1/platform/limits/)

## 8. Design/performance/accessibility targets

- Mobile first, few steps, clear swatches and material descriptions, on-page support; target image preview on slower Indian mobile networks. Avoid loading raw 50 MB originals in catalog views. Use responsive WebP/AVIF thumbnails where supported, compressed previews, lazy load, CDN cache and explicit dimensions to prevent layout shift.
- Define goals: LCP <2.5 s, CLS <0.1, INP <200 ms on representative field data; measure rather than promise. Public page accessible without JS where possible; keyboard-operable customizer, label every control, adequate contrast, descriptive validation and alt text.
- Admin PWA: optional install prompt; never cache private orders, customer photos, invoices or payment records in an offline service worker. Public storefront offline fallback only for safe static pages; checkout always online. Do not claim a PWA automatically makes a native app or offline commerce possible.

## 9. Implementation sequence and acceptance gates

| Phase | Build | Done when |
|---|---|---|
| 0 — discovery, 3–5 days | Supplier BOM/costs, photos, legal/tax review, supported pincodes, return/damage policy, brand/domain, provider accounts and payment/shipping eligibility. | Can produce a profitable manual quote for 3 representative sizes and know package weights/lead times. |
| 1 — foundations, ~1 week | Monorepo, two Pages deployments, Worker/D1 staging, auth/RBAC, migrations, CI, logging, backup and basic design system. | Owner signs in; non-staff gets 403; deployment/rollback and restore tested. |
| 2 — commerce, ~2 weeks | Catalog, customizer with upload/crop/resolution, server quote, cart, guest checkout, order creation, manual payment queue or gateway sandbox. | Test image can go from upload to immutable order with correct server-calculated amount. |
| 3 — fulfilment, ~1–2 weeks | Manager orders/production board, stock movements, QC, invoices, shipping label/tracking; notification templates. | Test paid order finishes print → QC → shipment with audit history and reversible exception flows. |
| 4 — launch hardening, ~1 week | Payment live + webhook retries, real delivery price/pincode, legal pages, SEO/prerender, mobile performance, security/abuse tests, analytics and real-user pilot. | 10–20 pilot orders reconciled end-to-end, refund/damage drill completed, no known critical security defects. |
| 5 — iterate | Reviews/UGC consent, gallery walls, volume pricing, premium materials, automated shipping, advanced reporting. | Add only after conversion, complaints, production time and margins are measured. |

**Initial KPIs:** customizer start→cart %, cart→paid %, photo rejection/remake %, average contribution margin per order, production SLA attainment, delivery damage %, support tickets/100 orders, and actual hosting/storage spend. “Better” should be measured against these, not asserted by aesthetics alone.

## 10. Open business decisions required before coding checkout

1. Which city/region can you manufacture and dispatch from, and which pincodes will you promise initially?
2. Do you own a physical framing/printing workshop or outsource? Get supplier price/BOM and packaging test results.
3. Will the first release use gateway checkout, manual UPI verification, COD, or a combination? What is the refund/damage policy?
4. What are your initial size/material/finish SKUs and realistic launch prices? The competitor prices above cannot substitute for your cost sheet.
5. Is adding a payment method acceptable? If **no**, prototype B2 uploads and delivery before choosing storage; do not assume R2/Oracle/Maps are available without billing setup.

**Recommended immediate first sprint:** settle those five decisions, obtain 10 original product photographs, build three realistic price/BOM examples, and prototype one private photo upload plus preview and one complete sandbox order. That validates the hardest risks before building dozens of marketing pages.

---

### Referenced provider documentation

[1](https://developers.cloudflare.com/pages/platform/limits/) Pages limits · [2](https://developers.cloudflare.com/workers/platform/limits/) Workers limits · [1](https://developers.cloudflare.com/d1/platform/pricing/) D1 pricing · [1](https://developers.cloudflare.com/d1/platform/limits/) D1 limits · [1](https://www.backblaze.com/cloud-storage/pricing) B2 pricing · [1](https://imagekit.io/plans/) ImageKit plans · [1](https://developers.cloudflare.com/r2/pricing/) R2 pricing · [2](https://developers.cloudflare.com/r2/get-started/) R2 setup · [1](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) OCI Always Free · [2](https://developers.google.com/maps/documentation/embed/quickstart) Maps Embed setup · [3](https://razorpay.com/blog/upi-charges-explained-mdr-vs-platform-fees/) gateway fee example · [1](https://help.delhivery.com/docs/client-developer-portal-1) Delhivery APIs · [3](https://developers.google.com/identity/verification/authentication-policy-compliance) Google identity production readiness.
