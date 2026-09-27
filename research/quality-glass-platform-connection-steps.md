# Quality Glass Emporium — platform connection sequence

**Starting point:** [Customer demo](framing-interface-demo.html) and [standalone manager demo](quality-glass-manager-demo.html). Both are **independent, client-only prototypes**. Changing an item in the manager demo does **not** change the customer demo; fictional orders, payment proofs and stock are not saved. Connection requires actual application code, authentication, backend and accounts. Never use either HTML demo to collect real money or screenshots.

## Confirm before provisioning

1. Decide whether the existing `quality-glass-website.vercel.app` will be replaced, kept temporarily, or redirected. Decide on a domain you own and can manage DNS for (example: `shop.yourdomain.in`, `manager.yourdomain.in`, `api.yourdomain.in`). Two `pages.dev` deployment URLs can be used first; buying a domain can wait.
2. Confirm the real shop WhatsApp number still is **+91 83031 08051**, and who will own the Cloudflare account. Do not send passwords or private keys in chat. Keep shop, manager and Git accounts under the business owner's control.
3. Select **Cloudflare R2** if you are willing to enable its subscription/payment setup; otherwise verify **Backblaze B2** account setup and signed upload/serve strategy. Use ImageKit only if resizing/CDN is needed; 20 GB monthly free bandwidth is a constraint, not universal free delivery. **Do not upload actual payment screenshots until private storage and staff access rules are implemented.**
4. Confirm the verified merchant **UPI ID/QR**, whose name appears to payers, whether the shop can review bank/UPI settlements, and the final shipping/tax/pricing policy. Never derive a UPI ID from the shop email or WhatsApp number. For two or more frames, obtain an owner-approved combined quote **before** inviting payment.
5. Use owned or appropriately licensed product/illustration assets. The anime-inspired and spiritual demo artwork is original placeholder imagery; the old catalog is not evidence of stock or character-image rights.

## The order to connect services

| Stage | Provider / outcome | Acceptance checkpoint |
|---|---|---|
| 1 | Cloudflare account + GitHub/GitLab repo; decide domain + Pages projects | Owner can sign in to own accounts. No tokens shared in chat. Determine whether the two standalone demos are prototypes only (recommended). |
| 2 | Scaffold real monorepo: `apps/shop`, `apps/manager`, `apps/api`, `packages/shared`, `db/migrations`; deploy **two** Pages projects | Public test URLs for both; builds controlled by owner. Cloudflare Pages Git integration accepts separate projects for a monorepo and needs each root/build/output configured. [1](https://developers.cloudflare.com/pages/get-started/git-integration/) React/Vite builds use `npm run build` → `dist` per app. [1](https://developers.cloudflare.com/pages/configuration/build-configuration/) |
| 3 | Deploy Worker API + **development D1**, then staging/production databases and migrations | `/health` returns healthy; manager login/roles enforced at API; one product listed from D1, not hard-coded in the browser. D1 is bound to Workers. [1](https://developers.cloudflare.com/d1/get-started/) |
| 4 | Choose private object storage: R2 or B2, then optional ImageKit public media | Customer image and proof have isolated private keys, server-validated MIME/size, short-lived uploads; manager sees only authorized order assets. |
| 5 | Implement real product, pricing, cart, multi-frame quote, order and payment-proof states | Single frame can checkout; 2+ frames require shop-approved total before payment; screenshot + UTR mean `pending_verification`, **not** paid. |
| 6 | Add verified owner UPI QR/ID; manual bank reconciliation, protected staff audit log | Staff marks paid only after checking merchant transaction. Duplicate UTR and mismatched amount cannot advance production. |
| 7 | WhatsApp final handoff + actual order confirmation/recovery | Message prefilled with order ID/items/UTR; chat still needs customer to press Send. If tab closes, order remains saved and trackable. Customer must manually attach screenshot in WhatsApp, or manager reads privately stored proof. |
| 8 | Delhivery account/API (when eligible), pincode/serviceability, booking, labels, tracking; optional Google login and Maps link | Test real sandbox serviceability/labels before production. Google OAuth can come later; guest checkout should work. |
| 9 | Analytics, backup/restore test, privacy/returns policy, accessibility, real pilot orders | Test failure paths and end-to-end reconciliation before directing customers to pay. |

**Security rule:** Place provider credentials in dashboard secrets/Worker secret bindings; keep local `.dev.vars`/`.env` out of Git. Cloudflare explicitly recommends secrets for sensitive keys. [1](https://developers.cloudflare.com/workers/configuration/secrets/) Manager site should never expose D1/R2/B2 keys in browser JavaScript. Installable PWA is optional after real functionality works.

## Step 1 to do together next

Reply with **(a)** whether you already own a domain or want temporary `pages.dev` URLs, **(b)** whether you have a GitHub account/repository and Cloudflare account, and **(c)** whether enabling R2 billing/payment setup is acceptable or you prefer B2. **Do not paste passwords, API tokens, QR screenshots or bank credentials.** Then we can scaffold the repo and configure the two Pages builds and Worker/D1 development bindings, one provider at a time.
