# Quality Glass Emporium — deployable workspace starter

Two free Cloudflare Pages **preview sites** and one **read-only** Worker API foundation live in this folder. No Cloudflare account or real database is connected yet. See [SETUP.md](SETUP.md) for exact steps.

## Ready now

- [Customer shop preview source](apps/shop/src/index.html) → safe Pages output ZIP: [`quality-glass-shop-pages-upload.zip`](quality-glass-shop-pages-upload.zip). The **deployed** shop output intentionally disables checkout; sample products and deal prices are not real offers.
- [Manager panel demo source](apps/manager/src/index.html) → Pages output ZIP: [`quality-glass-manager-preview-pages-upload.zip`](quality-glass-manager-preview-pages-upload.zip). **Public sample interface, not real admin access.** Never put private records in it.
- [Worker API](apps/api/src/index.mjs): `GET /health`, read-only categories/products once an owner's development D1 is attached; no orders, payments, admin writes or screenshots. [First catalog migration](apps/api/migrations/0001_catalog.sql) includes no seed products.

## Local build and tests

```bash
npm test
npm run build
# Optional after installing wrangler: npm install && npm run dev:api
```

The Python 3 build copies two self-contained HTML previews, with the shop checkout disabled in the **Pages build artifact**. The upload ZIPs already have `index.html` and `_headers` at the ZIP root for Cloudflare dashboard drag-and-drop. If you change the source later, rebuild and re-create the upload ZIPs; do not deploy an outdated ZIP. For future development, move inline CSS/JS and data URI images to a proper frontend build with separate static assets and content-security policy.

## Next owner action

**Credentials were disclosed in chat:** follow [recovery and GitHub Actions connection steps](docs/cloudflare-credential-recovery-and-connection.md) before any account connection. The repository includes a manually triggered [Pages preview deployment workflow](.github/workflows/deploy-pages-preview.yml), requiring newly created, narrowly scoped credentials kept **only in GitHub Actions secrets**. Alternatively use [SETUP.md](SETUP.md) to upload the two safe preview ZIPs manually. Share only the deployed `.pages.dev` URLs, never tokens, secrets or payment credentials. Later we can add the Worker, D1 and protected R2 storage in that order.
