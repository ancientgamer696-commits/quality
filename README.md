# Quality Glass Emporium — demos and platform plan

Public project handoff containing the current UI prototypes, research, and Cloudflare platform starter.

## Open the demos

- [Customer storefront demo](demos/customer-store.html) — collections, featured products, today's concept deals, customizer, and illustrative checkout flow.
- [Manager panel demo](demos/manager-panel.html) — fictional orders, production board, catalog, payment-review simulation and reporting.

The demos are standalone HTML files. Open/download them in a browser. **They do not take payments, upload screenshots, store orders, or connect to your Cloudflare account.** The public Pages shop build in `platform/` disables checkout; the manager preview is not a secure login.

## Plans and implementation

- [Competitor review and complete system plan](research/framing-ecommerce-research-and-build-plan.md)
- [Animation and multi-page blueprint](research/framing-animation-and-multipage-blueprint.md)
- [Shop details and manual-payment requirements](research/quality-glass-shop-details-and-payment-requirements.md)
- [Platform integration sequence](research/quality-glass-platform-connection-steps.md)
- [Cloudflare platform starter and setup instructions](platform/README.md)
- [Original placeholder artworks](assets/) — illustrative assets, not confirmed shop inventory.
- [Structured extracted data](data/README.md) — old-site category/product snapshots, cited competitor observations, provider limits, shop profile and feature requirements. **Not** an approved product import.

No API tokens, R2 keys, customer payment proof, or private data should ever be committed to this public repository.

> GitHub Actions workflow is at [`.github/workflows/deploy-pages-preview.yml`](.github/workflows/deploy-pages-preview.yml), adapted for this repository layout. It requires new GitHub Actions secrets and is manual-only. Do not reuse any credentials pasted in chat.
