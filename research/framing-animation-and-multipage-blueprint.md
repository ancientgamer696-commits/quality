# Framing website — animation research and multi-page expansion

**Research date:** 27 September 2026 · **Companion to:** [full commerce/backend plan](framing-ecommerce-research-and-build-plan.md). This document adds a concrete site map and motion specification for **two websites**: a public customer store and a private manager panel. The page examples below are **proposed designs** unless explicitly labeled as observed competitor content; text extraction of competitor sites cannot establish how their animations actually run in a browser.

## Decision in one minute

- Build a **multi-page customer storefront** with distinct pages for discovery, guided framing, product details, materials/pricing trust, checkout and post-purchase tracking. Build a separate **multi-section manager website** for orders, production, stock, pricing and reports.
- Make the **frame builder the visual signature**: instantly show the uploaded photo inside a selectable moulding and mat, while visibly updating dimensions, crop-quality advice and the server-quoted total. Motion should explain an action or changed state—not obstruct it.
- Start with **CSS transitions and tiny amounts of client-side JavaScript**; add Motion for React for the builder and selective UI state transitions if needed. Keep complex GSAP storytelling and Rive off the critical buying path. Cross-document View Transitions can be a progressive enhancement; normal links still work.
- **No animated intro, no auto-advancing essential carousel, no parallax-heavy checkout, no animation prerequisite for navigation.** Honor reduced-motion settings and provide a site-level motion toggle if significant decorative motion is added.

## 1. Additional competitor observations relevant to page structure

| Public evidence | Page-design lesson | What is *not* established |
|---|---|---|
| [Framebridge: How it works](https://www.framebridge.com/pages/how-it-works) uses examples of framed vs unframed items; its [materials page](https://www.framebridge.com/pages/materials) breaks down moulding, backing, paper, mat, glazing and hardware. | Create **How it works** and **Materials & quality** pages with original before/after imagery and a small, user-controlled visual reveal. | We did not inspect or validate the actual transition/hover animation of their site. |
| [Framebazaar's bestseller category](https://framebazaar.com/collections/best-selling-frames) has price/color/style filters; [Osaka product](https://framebazaar.com/products/osaka-frame) offers options, upload and preview. | Keep a dedicated listing page and a separate focused product/builder flow. Animate only filter drawer, selection feedback and preview swap. | We cannot infer its client-side implementation or real animation performance. |
| [VistaPrint's design gallery](https://www.vistaprint.in/photo-gifts/photo-with-frame/templates) offers searchable templates and facets (size, color, style, orientation); its [product page](https://www.vistaprint.in/photo-gifts/photo-with-frame) also offers upload. | Add an occasion/template gallery **later**, and make “Start with your own photo” prominent on launch. | Template count/results and prices are time-dependent; no proof of actual interaction motion. |
| [CanvasChamp framed prints](https://www.canvaschamp.in/framed-prints) exposes size/frame/paper/mat choices on its public page. | Present options as an ordered builder instead of showing all combinations at once. | Public text does not tell us whether its live preview updates on each option. |

**Differentiation principle:** A more efficient site is not one with *more animations*. It is one that helps a shopper understand the result, pay with confidence and find support faster.

## 2. Customer website: full proposed page map

Legend: **P0** = needed for first paid order; **P1** = strong launch follow-up; **P2** = later. Paths are examples; keep slugs readable and canonical. Public marketing/product pages should render meaningful HTML without depending solely on client JavaScript. Cart, account and builder are interactive.

### A. Discover and choose

| Priority | Route and page | What it must contain | Motion with a purpose |
|---|---|---|---|
| P0 | `/` **Home** | One main CTA “Upload & frame”; choose Photo / Empty frame / Certificate; top sellers; 3-step story; honest starting prices; delivery/quality proof; FAQ. | Subtle hero photo→framed reveal **on button press**, not an unskippable video; brief section fades after content is visible. |
| P0 | `/start` **What are you framing?** | Choice cards: digital photo, empty ready-made frame, physical art/certificate quote; clear route into correct flow. | Selection border/scale ≤180 ms; preserve selection when using Back. |
| P0 | `/shop` **All frames** | Search, price/size/material/color filters, sort, product count, responsive cards. | Filter drawer enters; selected chips change; product grid updates without jumping. |
| P0 | `/collections/:slug` **Category** | One SEO-friendly intro, filters and related products; e.g. `/collections/wooden-frames`, `/collections/tabletop-frames`. | Same listing motion; don't invent dozens of thin SEO pages. |
| P0 | `/products/:slug` **Product detail** | Real photos, exact dimensions (art opening + outer size), composition, price range, variants, ETA/pincode, reviews if authentic, returns. | Image cross-fade and color swatch transition without flashing. |
| P1 | `/gifts` and `/gifts/:occasion` **Gift guide** | Birthdays, anniversaries, weddings, parents; gift-ready SKUs, message option and realistic delivery promise. | Soft card feedback and optional before/after; no seasonal confetti on every visit. |
| P2 | `/gallery-walls` **Gallery wall configurator** | Layout presets, wall size guide, 2–6 frame previews, bundle price; operationally complex. | Drag/resize only if keyboard alternative and correct dimensions/pricing exist. |
| P2 | `/templates` **Design templates** | Original licensed occasion templates, size/style filters; each template leads to customization. | Preview swap; no auto-scrolling carousel. |

### B. Customize and buy

| Priority | Route and page | What it must contain | Motion with a purpose |
|---|---|---|---|
| P0 | `/frame/create` **Guided builder** | Stages: upload → crop/size → frame finish → mat/paper/glazing → review; preview + live price; save draft. Route can encode a draft token, not raw customer image URL. | User-selected photo fits into a composited frame; 120–200 ms swatch preview; directional step change 180–240 ms. Never animate the *price value* deceptively; update text immediately. |
| P1 | `/frame/preview/:draftId` **Full-screen preview/review** | Side-by-side room mockup vs neutral crop, actual print dimensions and low-resolution warning, explicit crop approval. Auth/opaque token needed; not search-indexable. | User-controlled compare slider; reduced-motion fallback is a static toggle. |
| P0 | `/cart` **Cart** | Editable configuration, preview, quantity, coupon, estimated shipping and tax summary; return to builder without losing settings. | Removal collapses only the removed row; totals update immediately and accessibly. |
| P0 | `/checkout` **Checkout** | Contact/address/pincode, fulfilment promise, shipping/tax/total, payment choice, policies and consent. | Almost none: instant validation, brief spinner only for real network operation. |
| P0 | `/order/confirmation/:token` **Confirmation** | Order reference, payment state (paid vs pending verification), expected next steps and support link. | One optional celebratory checkmark ≤500 ms; never show success until server confirms it. |
| P0 | `/track` and `/track/:token` **Track** | Secure lookup, status timeline, courier tracking and exception/help path. | Newly completed step appears; timestamps stay visible even without animation. |
| P1 | `/checkout/payment-pending` **Pending payment** | Bank transfer/UPI reference and manual verification message, retry/contact. | No falsely reassuring “paid” animation. |

### C. Build trust and support

| Priority | Route and page | What it must contain | Motion with a purpose |
|---|---|---|---|
| P0 | `/how-it-works` **Process** | 3 steps + production/dispatch reality; one clear CTA at every stage. | Short, opt-in before/after slider or step illustration. |
| P0 | `/materials` **Frame anatomy** | Moulding, mat, backing, paper, glazing, hanging hardware; comparisons and real photographs. | Click an anatomy hotspot to highlight its label; **not** 3D/WebGL for launch. |
| P0 | `/pricing` **Price explained** | Sample configurations and what changes price; true itemized builder quote, delivery/tax treatment. | Instant accordion expansion and calculator selection feedback. |
| P0 | `/shipping` **Shipping & delivery** | Pincode/service area, timelines, packaging, damage claim process. | Pincode result appears with text, not color alone. |
| P0 | `/help` **FAQs** | Upload/file quality, sizes, turnaround, payment, changes, replacement, contact. | Accordion ≤180 ms; accessible keyboard controls. |
| P0 | `/contact` **Contact / WhatsApp** | Address, opening hours, support form, wa.me link, map link; custom-size enquiry. | Form confirmation only after submitted successfully. |
| P0 | `/about` **Our workshop** | Genuine team/workshop images, location, craftsmanship and honest capabilities. | Optional scroll fade on non-critical media only. |
| P0 | `/privacy`, `/terms`, `/returns`, `/cancellation` **Policies** | Real policy content; photo retention, custom goods, claims, cancellation windows. | None. Readability wins. |
| P1 | `/corporate` **Bulk/corporate enquiries** | Volume pricing and quote request, lead time and tax invoice expectations. | None beyond form success. |
| P1 | `/guides/:slug` **Buying guides** | Print quality, sizing, wall mounting, certificates and materials; useful original content. | Optional interactive size comparison. |

### D. Customer account (guest checkout remains possible)

| Priority | Route | Purpose |
|---|---|---|
| P1 | `/account/login` | Google sign-in or guest order lookup; clear privacy explanation. |
| P1 | `/account/orders` and `/account/orders/:id` | Status, item details, invoice and support. |
| P1 | `/account/profile` | Addresses, preferences, consent controls and deletion request. |
| P1 | `/account/saved-designs` | Resume draft only if storage/security policy supports it. |

**Launch total:** ~18 page templates plus dynamic product/category instances; not 18 entirely different codebases. A small set of reusable layouts (editorial, listing, product, builder, transactional, account) keeps implementation efficient. Product variants and filters should **not** generate duplicate indexable pages automatically.

### Navigation proposal

```text
Header:  Upload & Frame | Shop Frames | Gifts | How it Works | Materials | Support | Account | Cart
Mobile:  Menu + visible Upload CTA + Cart
Footer:  About | Pricing | Shipping | Policies | Contact | Location | Social
```

Suggested cross-page journeys:
- **Fast:** Home → Builder → Cart → Checkout → Confirmation.
- **Researching:** Category → Product → Materials → Builder → Cart.
- **Gift:** Gifts → Occasion → Product → Builder → Checkout.
- **Physical artwork:** Start → Request quote → Staff responds → Approved quote → Payment.
- **Support:** Track → Problem/damage form → Manager ticket and resolution.

## 3. Manager website: full proposed page map

Manager is a **separate private site** (e.g. `manager.example.in`). It is not indexed; login/role checks protect API data; saving admin work must never depend on animations.

| Priority | Route and screen | Core task | Appropriate motion |
|---|---|---|---|
| P0 | `/login` | Staff login; role validation; session expiry. | None except input feedback. |
| P0 | `/dashboard` | Action queues: artwork check, pending payments, late jobs, ready to dispatch. | Updated counts highlight briefly; do not scroll-jump as data refreshes. |
| P0 | `/orders` | Search/filter by date/status/payment; bulk actions with confirmation. | Filter panel 150 ms; new row highlight, avoid heavy row reordering. |
| P0 | `/orders/:id` | Item snapshot, crop/private image, address, payment evidence, customer notes, state history, actions. | Status badge change + success toast only after API succeeds. |
| P0 | `/production/board` | Artwork review → printing → framing → QC → packing; owner assignment and SLA. | Optional drag/drop, but **buttons/menus + keyboard** always supported; optimistic transition only with rollback. |
| P0 | `/catalog/products` and `/catalog/products/:id` | Create/edit/publish product, options, photos and visibility. | Save-state indicator and local preview; no animation during critical editing. |
| P0 | `/pricing` | BOM, size rules, taxes, margins, versioning and draft→publish. | Before/after price diff highlighted; require confirmation. |
| P0 | `/inventory` and `/inventory/movements` | Moulding/paper/glazing/hardware stock and audit trail. | Low-stock status signal; never color-only. |
| P0 | `/payments` | Gateway reconciliation or manual UPI verification. | Explicit pending→verified transition *after backend proof*, with actor/time. |
| P0 | `/shipping` | Serviceability, labels, waybills, pickups, NDR/returns. | Timeline refresh but no live moving decorations. |
| P1 | `/quotes` | Custom dimensions, physical-art intake, approval and customer follow-up. | Quote sent confirmation. |
| P1 | `/customers` and `/customers/:id` | Order history, tickets, consent and restricted PII. | None beyond transitions between tabs. |
| P1 | `/support` and `/support/:id` | Damages/replacements, SLA and evidence. | Notification only for new tickets. |
| P1 | `/reports` | Sales, margins, wastage, conversion, dispatch SLA. | Charts animate **once only** if helpful; table export available. |
| P1 | `/content` | FAQs, home banners, guides, policies, review moderation. | Preview/publish state feedback. |
| P1 | `/team`, `/settings`, `/audit` | Staff RBAC, shipping/payment settings and change history. | Avoid motion on security-sensitive confirmations. |

**Admin information architecture:** left navigation (Overview, Orders, Production, Catalog, Pricing, Inventory, Payments, Shipping, Quotes, Support, Reports, Settings); contextual search and filters; persistent breadcrumbs. On mobile, prioritize read/status updates; complex bulk tasks can have a desktop-first layout if usable alternatives remain.

## 4. Animation strategy and interaction specifications

### Motion tokens (initial proposal; test with real users)

| Token | Default | Intended use |
|---|---|---|
| `instant` | 0–80 ms | Price text and eligibility/status changes; should feel immediate. |
| `micro` | 120–180 ms ease-out | Swatch selection, hover/focus feedback, button state. |
| `panel` | 180–240 ms ease-out | Filter drawer, builder step, cart row or FAQ. |
| `reveal` | 250–350 ms max | Non-essential decorative reveal in editorial sections. |
| `success` | ≤500 ms once | Order confirmed or file upload completed; only on real completion. |

**Principles:** never delay access to the next task for a flourish; don't use motion to hide a slow API; animate `transform` and `opacity` when possible, not frequently changing `width`, `height`, `left` or `top`. Google’s performance guidance specifically recommends compositor-friendly properties to avoid layout/paint work. [1](https://web.dev/articles/animations-guide)

### The signature interaction: frame-builder visual storyboard

1. **Before upload:** An empty sample frame remains visible. “Choose a photo” is a real labelled file input; a static example illustration explains crop.
2. **Upload:** Show true progress if the upload API provides measurable progress, else an indeterminate progress indicator with a plain text “Uploading”; do not pretend progress reaches 100%. Keep original private; create a lightweight in-browser preview immediately.
3. **Photo arrival:** Fit photo inside an SVG/CSS frame mask; preserve image aspect ratio; detect rotation; show crop boundary. Fade only the photo layer (~180 ms). If image is low resolution for selected print size, show a persistent warning with pixel numbers and suggested alternatives.
4. **Choose size:** Frame’s proportion changes; show both **image opening** and **outer frame** with labels. Resize the illustrative preview without moving the rest of the page; no inaccurate 3D room scale.
5. **Select moulding and mat:** Swap a small set of original photo/video-free textures or vector layers. The selected option gets visible outline + text + aria-pressed; the frame layer cross-fades/changes rapidly. Price updates from the server quote; don't rely on a client-side animated number as the source of truth.
6. **Crop edit:** Drag/zoom/rotate with keyboard buttons and a numerical zoom control, plus Undo/Reset. Debounce expensive rendering; persist normalized crop coordinates, not just a preview screenshot. A change to crop should never silently reset chosen print size.
7. **Review:** Display static final composition, dimensions, material breakdown, tax/shipping status, risk warning, and a checkbox/explicit confirmation of approved crop. Only now enable Add to cart.

**Composition implementation:** use standard `<img>` or `<canvas>` only inside the editor for local display, CSS/SVG overlay layers for moulding/mat, original image retained privately, crop data and variant IDs sent to backend. Actual print-ready output should be rendered/checked by the production pipeline, not derived from a compressed marketing mockup. Lazy-load interactive builder JS only on builder routes.

### Recommended animations by page family

- **Home/editorial:** Subtle heading fade or framed/unframed switch on click. No automatic hero carousel; one strong static hero often converts better than an uncontrolled slideshow (**hypothesis to test**, not an observed performance fact).
- **Listings:** Filter drawer and chips; optional product-card finish preview on hover **and** tap/focus; no movement of every card on scroll.
- **PDP:** Thumbnail cross-fade, swatch selection, small sticky buy bar on mobile; no simulated “only 2 left” urgency unless stock truly backs it.
- **Builder:** Motion communicates chosen material, crop, dimension and flow step. Keep selections responsive even on weak devices.
- **Checkout/legal:** Nearly static; plain feedback, real progress, stable layout.
- **Order tracking/admin:** Motion emphasizes a legitimate state transition; record actor/timestamp and allow the event to be read without animation.

## 5. Implementation research: what to use and when

| Technology | Fit for this project | Risk/guardrail |
|---|---|---|
| **CSS transitions/keyframes + IntersectionObserver** | Default for nav, buttons, filters, FAQ, non-critical editorial reveals. Zero animation-library requirement. | Mark reveal content visible by default; only enhance after JS and observer are ready so broken JS cannot hide content. |
| **Motion for React** | Good for interactive builder step changes, swatches/layout transitions and manager drawers. Docs provide site-wide `MotionConfig reducedMotion="user"`, `useReducedMotion` and `LazyMotion` to defer features. [1](https://motion.dev/docs/react-motion-config) [3](https://motion.dev/docs/react-reduce-bundle-size) | Import only in routes that need it; avoid heavy general motion bundle on static product pages. |
| **View Transitions API** | Native progressive enhancement for same-document UI changes; cross-document transitions can link same-origin static pages with `@view-transition { navigation: auto; }`. [1](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API/Using) | **Cross-document support is not universal** as of current MDN guidance; ordinary navigation must remain correct. Different origins (shop vs manager) cannot share the cross-document transition. [2](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@view-transition) |
| **GSAP + ScrollTrigger** | Reserve for a later campaign or one carefully controlled materials story. Its `matchMedia()` can apply desktop/mobile/reduced-motion conditions. [1](https://gsap.com/docs/v3/GSAP/gsap.matchMedia()/) | Often overkill for checkout; scroll-driven hero effects can distract or hurt mobile performance. Check current licensing/bundle before adoption. |
| **Lottie / Rive** | Optional single custom illustration for success or “How it works,” only after asset/bundle testing. Lottie is animation JSON runtime; Rive has interactive runtimes. [1](https://airbnb.io/lottie/) [1](https://rive.app/docs/runtimes/getting-started) | Runtime/export/asset licensing and accessibility need review. Rive runtime being open-source does **not** imply every designer export/asset is free. Neither is necessary for P0. |

**SEO note:** Google recommends putting merchant Product structured data in **initial HTML** where possible; client-only generated markup can be less reliable for changing prices/availability. Animate *on top of* already rendered accessible content, not in place of it. [2](https://developers.google.com/search/docs/appearance/structured-data/product-snippet)

### Reduced-motion and control requirements

- Respect `prefers-reduced-motion: reduce`; remove large translations/parallax and autoplay, keep essential state changes instantaneous or simple fade. MDN documents the media query and its accessibility purpose. [1](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Media_queries/Using_for_accessibility)
- If a marketing carousel or ongoing animation is ever introduced, make it pause/stop/hide-able. WCAG 2.2 requires controls for certain moving content that starts automatically and lasts >5 seconds; interaction-triggered nonessential motion is also addressed at AAA. [2](https://www.w3.org/TR/WCAG22/#pause-stop-hide) [2](https://www.w3.org/TR/WCAG22/#animation-from-interactions)
- Never use flashing effects. Motion cannot be the only channel for progress, error, low-quality photo warnings, stock status, or admin order changes. Give keyboard access to swatches, compare slider, drag alternatives and dialogs; manage focus after modal/route changes.
- With JS motion libraries, the reduced-motion preference must also be checked in JS: CSS alone will not necessarily disable JS-driven animation. If offering a “Reduce animations” toggle, store preference locally and apply on both sites independently.

### Example CSS starter (progressive enhancement)

```css
:root { --motion-fast: 160ms; --motion-panel: 220ms; }
.swatch, .button { transition: transform var(--motion-fast) ease-out, opacity var(--motion-fast) ease-out; }
.swatch:hover { transform: translateY(-2px); }
.swatch:focus-visible { outline: 3px solid #165d65; outline-offset: 3px; }
/* Only opt in if feature tested in your target browsers; normal links are the fallback. */
@view-transition { navigation: auto; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { scroll-behavior: auto !important; animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

Avoid a site-wide hard animation reset if it breaks essential loading or focus behavior; test the specific UI. Page transitions must not replay on form resubmission or hide native browser Back/Forward behavior.

## 6. Practical design directions — pick one brand language

These are **design proposals**, not existing competitor facts.

| Direction | Visual ingredients | Best for | Motion mood |
|---|---|---|---|
| **Warm Craft Studio** (recommended) | Off-white canvas, walnut/charcoal text, restrained brass accent, generous whitespace, honest workshop photographs, serif display + readable sans body. | Gift buyers and premium-but-accessible framing. | Quiet fades and tactile frame selection. |
| **Modern Gallery** | Neutral gallery white, black/steel frames, editorial grid, larger art mockups and strong typography. | Home décor and design-conscious buyers. | Minimal image swaps; almost invisible page transitions. |
| **Playful Gift Shop** | Brighter color chips, occasion illustrations, preset designs and vibrant packaging. | Birthdays, collages and lower-priced gifting. | Bouncier micro-feedback only; keep checkout calm. |

**Choose one** before photography/UI build. Do not use competitor logos, copyrighted art or their product photos. Photograph your own mouldings from consistent angle and lighting; prepare transparent frame overlays, product-on-wall scale mockups, swatch textures and a few close-up material shots. These assets matter more than advanced animation libraries.

## 7. Delivery plan for multiple pages and animation

| Sprint | Output | Acceptance test |
|---|---|---|
| 1 — IA + design (3–5 days) | User flows, page inventory, navigation tree, 6 reusable page templates, brand direction, 4–6 frame sample assets, wireframes for home/builder/PDP/checkout/admin board. | Everyone can reach a builder or product in ≤2 meaningful choices; no dead-end routes. |
| 2 — public P0 pages (1–2 weeks) | Home, start, shop, category, PDP, materials/how-it-works/pricing, shipping/help/contact/policies; meaningful initial HTML. | Search engines and no-JS browsers can read the important catalog/help content; keyboard navigation works. |
| 3 — builder + commerce (1–2 weeks) | Upload/crop, preview layers, quotes, cart, checkout, order success/tracking. Add only functional motion. | Mobile test photo→approved frame→paid or pending order succeeds even with reduced motion and without View Transitions support. |
| 4 — manager P0 (1–2 weeks) | Dashboard, orders, detail, production, catalog, price rules, stock, payment/shipping. | Staff can process a complete test order without losing state; role restrictions verified. |
| 5 — polish + P1 | Review pilot recordings/analytics, fix friction, then gift pages, quotes, account, support and one optional motion story. | Motion measurably clarifies task and does not regress mobile performance or accessibility. |

**Performance guardrails (targets, not promises):** page LCP <2.5 s, CLS <0.1 and INP <200 ms on representative mobile field data; compare with/without animations on mid-range Android and slow 4G. Reserve image dimensions, lazy-load below-fold imagery, prefetch conservatively, avoid fetching customer originals merely to show catalog cards. Track builder step completion and abandonment, not just page views. Baselines should be measured before claiming an animation improves conversion.

## 8. Recommended next build artifact

Create a clickable **wireframe/prototype** for these eight representative screens before building all pages: `Home → Start → Category → Product → Frame builder → Cart → Checkout → Order status`, plus an admin `Orders → Production` pair. Define reusable components (header/footer, product card, filter drawer, frame preview, quote summary, status timeline, admin table). Validate those flows with 5–10 real prospective buyers and one workshop operator. Then implement P0 routes; P1/P2 pages should be driven by observed demand.
