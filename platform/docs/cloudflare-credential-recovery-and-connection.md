# Connect Cloudflare safely after credentials were exposed

**Immediate action:** Cloudflare API tokens and an R2 Access Key/Secret Access Key pair were pasted into a conversation. Assume all pasted secret values are compromised. **Do not use those credentials for deployment, storage access, a curl verification request, or GitHub secrets.** Do not copy them into a repo, `.env` file, deployment log, support ticket, or another chat.

## 1. Revoke first (in your own Cloudflare dashboard)

1. Cloudflare dashboard → **Manage Account → API Tokens** (or **My Profile → API Tokens** if the credential was created as a user token). Locate the newly disclosed token by its label/date and **revoke/delete** it. You do not need to copy its secret to identify it. Cloudflare token docs: <https://developers.cloudflare.com/fundamentals/api/get-started/create-token/>.
2. Cloudflare dashboard → **R2 object storage → Overview → Account Details → API Tokens → Manage**. Locate and revoke/delete the R2 token/key pair that produced the disclosed Access Key ID and Secret Access Key. Some R2 tokens are also Cloudflare account/user API tokens, so check **both** locations without assuming they are independent. Docs: <https://developers.cloudflare.com/r2/api/tokens/>.
3. If these credentials were used for an existing site, app, GitHub secret or storage client, update those applications to newly created credentials. Inspect recent token/R2 activity and object changes in the dashboard if available; ask Cloudflare support if you see unexpected access. Enable Cloudflare and GitHub 2FA.

## 2. Use a fresh, limited Pages token without giving it to this workspace

Create a **new** custom Cloudflare account API token with only **Account → Cloudflare Pages → Edit**, scoped only to your Quality Glass account. This token deploys the two preview sites; it is **not** an R2 S3 access key. See Cloudflare's Pages CI guide: <https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/>.

Create a GitHub repository you own, with **the contents of `quality-glass-platform` at the repository root**. Upload/push this project after checking that no `.dev.vars`, `.env`, logs, keys or screenshots are included. The prepared workflow is `.github/workflows/deploy-pages-preview.yml`.

In that GitHub repository → **Settings → Secrets and variables → Actions → New repository secret**, add:

- `CLOUDFLARE_PAGES_TOKEN` = your **new** limited Pages token. Enter it **only** in GitHub, not here.
- `CLOUDFLARE_ACCOUNT_ID` = your Cloudflare account ID (not a secret in the same sense as a token, but place it in Actions secrets for convenient configuration). Do not confuse an account ID with a token or R2 key.

First create two Cloudflare Pages **Direct Upload** projects in dashboard (empty or using safe previews): `quality-glass-shop` and `quality-glass-manager-preview`. If a name is taken, tell me the actual project names and I'll update workflow project names *before running it*. Cloudflare's Direct Upload guide: <https://developers.cloudflare.com/pages/get-started/direct-upload/>.

Then in GitHub → **Actions → Deploy safe Quality Glass Pages previews → Run workflow**. It builds from source and deploys both sites; the public shop build disables checkout, and the manager build is a **fictional public demo**. No real admin access, payment collection, API/R2 connection, or private records are involved. Cloudflare Pages CI guide: <https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/>.

## 3. R2 later, not from the leaked S3 credentials

For a Worker, create a private R2 bucket under your account once the billing/subscription is enabled and your login is secure. Use a **Worker R2 binding** rather than pasting a S3 Access Key/Secret Key into code or CI. R2 binding documentation: <https://developers.cloudflare.com/r2/api/workers/workers-api-usage/>. We will not enable customer-original or payment-proof uploads until the backend has proper order IDs, server-side staff auth, size/MIME validation, private access, retention and audit logging.

## What to report back (not secrets)

After revocation: **"revoked"**; and when created, the *repository URL* and the *two public `.pages.dev` URLs*. Do **not** send any new token, R2 secret, login code, screenshot of credential screens, or QR/private payment information.
