# Full-system launch gates (Quality Glass Emporium)

**Requested goal:** two sites + Worker API + D1 + R2 + manual UPI screenshot verification + WhatsApp handoff. Current status: independently tested preview sites + read-only Worker. No provider account connection has occurred in this workspace; no credentials were supplied.

## User-supplied business materials required

- Approved catalog: complete [`product-catalog-template.csv`](product-catalog-template.csv) or provide a spreadsheet with the same fields. Upload product photos you own or are licensed to sell. Anime franchise characters and reproductions require rights; never publish unlicensed examples as stock. A framed print also needs verified production dimensions, supplier cost, pricing, tax treatment, fulfilment time and quantity.
- Verified shop-owned UPI QR/ID and payee name: supply securely to **your Cloudflare-controlled dashboard**, not this public workspace or chat. Test a small transaction from your own phone first; confirm payee identity.
- Verify whether WhatsApp +91 83031 08051 is your actual business account, and confirm delivery/pickup geography, packaging and shipping costs.
- Cloudflare Pages production origins assigned to shop and manager; GitHub repository if using automatic builds; Cloudflare account owner handles authorization.

## Engineering sequence

1. Pages previews live, manager demo publicly marked as demo, no payment collection. Unauthenticated manager SPA is **not** an admin website.
2. D1 development DB + read-only catalog API. Verify migrations and published flags; no real customer data yet.
3. Real admin auth: owner login, controlled staff allowlist, signed httpOnly sessions/cross-origin handling, CSRF and RBAC, audit trail. Replace demo manager with authenticated API client. Protect Pages URL via access gateway if desired, but gateway alone is not API authorization.
4. Private R2 bucket: enable Cloudflare R2 subscription yourself, bind bucket to Worker; allow only authenticated/authorized uploads/downloads with opaque object keys, MIME/size/quantity validation, malware/PDF strategy, short retention and signed access. No public payment screenshots. Route images directly to bucket using signed upload technique when appropriate; don't relay large originals through free Worker without testing.
5. Real catalog editor and storefront from D1. Prices server-owned and approved. Do not trust the previous static UI example prices.
6. Quote/cart/orders: fixed price snapshots, one-frame checkout allowed; 2+ frames require owner-approved final quote before payment, including shipping/taxes; order reference must be securely generated and persisted. Accurate fulfilment policy.
7. Verified UPI payee display; manual proof submission stays `pending_verification`. Staff checks actual merchant statement and UTR uniqueness; no `paid` until independent verification. Missing WhatsApp Send, duplicate proof, mistaken payment, partial payment, refund, failed upload, contact change, and abandoned order need handling.
8. WhatsApp `wa.me` prefilled message with order ID, items, UTR, explicit pending status. Customer taps Send; attaching screenshot to chat is manual. Store privately in manager if already uploaded to R2.
9. Shipping account/serviceability/labels and optional login/map; recovery/backups/security review and small real-order pilot before launch.

**Do not promise “all platforms connected and working” until the Cloudflare account actually contains two deployed Pages sites, Worker with real D1 and R2 bindings, authenticated owner login, tested payment review and staged order acceptance.**
