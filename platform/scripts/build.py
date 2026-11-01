#!/usr/bin/env python3
"""Copy one self-contained demo into a Cloudflare Pages output directory.

Using only Python stdlib means Pages can build immediately without npm installs.
The manager output is intentionally a DEMO, not a secure admin application.

Shop builds additionally get the full Open Graph / link-preview set:
  - site-level og: + twitter: meta injected into index.html
  - real image files extracted from the inlined data-URI art
  - /share/<slug>/ stub pages per product and category so links shared on
    WhatsApp/Facebook render a rich card with that exact product's photo.
"""
import base64
import html
import os
import pathlib
import re
import shutil
import sys

root = pathlib.Path(__file__).resolve().parents[1]
if len(sys.argv) != 2 or sys.argv[1] not in {"shop", "manager"}:
    raise SystemExit("Usage: python3 scripts/build.py shop|manager")
app = root / "apps" / sys.argv[1]
source = app / "src" / "index.html"
output = app / "dist"
if output.exists():
    shutil.rmtree(output)
output.mkdir(parents=True)
content = source.read_text()

SITE = os.environ.get("QGE_ORIGIN", "https://quality-glass.pages.dev").rstrip("/")

DESC = ("Handmade frames, LED mirrors, mandir & god frames, custom glass work in Raebareli. "
        "Browse the collection, order on WhatsApp, doorstep pickup.")

if app.name == "shop":
    # The shared preview is deliberately browsable, not a payment collector.
    # Local src/index.html remains an interactive UI prototype. Publishing a
    # functional payment-proof form before backend/order storage would mislead
    # customers into submitting genuine UTRs with nowhere secure to store them.
    content = content.replace(
        'data-go="checkout">Continue to checkout ↗</button>',
        'disabled title="Preview only; checkout is not yet connected">Checkout unavailable in public preview</button>',
    )
    assert "Checkout unavailable in public preview" in content
    content = content.replace(
        '· Interactive prototype · No live payments or uploads',
        '· Public preview · Checkout disabled · No live payments or uploads',
    )

    # ---------- extract embedded art to real files (for og:image) ----------
    ogdir = output / "og"
    ogdir.mkdir(exist_ok=True)
    arts = {}
    for name in ("HERO", "ANIME", "SACRED", "ABSTRACT", "ART"):
        m = re.search(name + r"\s*=\s*'data:image/jpeg;base64,([^']+)'", content)
        if m:
            raw = base64.b64decode(m.group(1))
            fn = f"{name.lower()}.jpg"
            (ogdir / fn).write_bytes(raw)
            arts[name] = f"{SITE}/og/{fn}"
    (output / "og-cover.jpg").write_bytes((app / "src" / "og-cover.jpg").read_bytes())
    cover = f"{SITE}/og-cover.jpg"

    # ---------- site-level OG + twitter meta ----------
    og_block = (
        '<meta name="description" content="{desc}">'
        '<link rel="canonical" href="{site}/">'
        '<meta property="og:site_name" content="Quality Glass Emporium">'
        '<meta property="og:type" content="website">'
        '<meta property="og:locale" content="en_IN">'
        '<meta property="og:url" content="{site}/">'
        '<meta property="og:title" content="Quality Glass Emporium — Frames · LED Mirrors · Mandir Decor, Raebareli">'
        '<meta property="og:description" content="{desc}">'
        '<meta property="og:image" content="{cover}">'
        '<meta property="og:image:width" content="1200">'
        '<meta property="og:image:height" content="630">'
        '<meta property="og:image:alt" content="Gold-framed art wall by Quality Glass Emporium">'
        '<meta name="twitter:card" content="summary_large_image">'
        '<meta name="twitter:title" content="Quality Glass Emporium — Raebareli">'
        '<meta name="twitter:description" content="{desc}">'
        '<meta name="twitter:image" content="{cover}">'
    ).format(desc=html.escape(DESC, quote=True), site=SITE, cover=cover)
    if "<title>" in content:
        content = re.sub(r"(<title>.*?</title>)", r"\1" + og_block, content, count=1)

    # ---------- per-product & per-category share stubs ----------
    def slugify(t):
        return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

    def stub(pdir, title, desc, image, url, kind="product"):
        d = output / "share" / pdir
        d.mkdir(parents=True, exist_ok=True)
        t, ds, im = html.escape(title, quote=True), html.escape(desc, quote=True), html.escape(image, quote=True)
        page = (
            "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\">"
            f"<title>{html.escape(title)}</title>"
            f'<meta name="robots" content="noindex">'
            f'<meta property="og:type" content="{kind}">'
            '<meta property="og:site_name" content="Quality Glass Emporium">'
            f'<meta property="og:url" content="{url}">'
            f'<meta property="og:title" content="{t}">'
            f'<meta property="og:description" content="{ds}">'
            f'<meta property="og:image" content="{im}">'
            f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            '<meta name="twitter:card" content="summary_large_image">'
            f'<meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{ds}">'
            f'<meta name="twitter:image" content="{im}">'
            f'<meta http-equiv="refresh" content="0;url={SITE}/">'
            f'</head><body style="font-family:system-ui;background:#f8f6f1;color:#41506b;padding:40px">'
            f'{html.escape(title)} — opening shop…</body></html>'
        )
        (d / "index.html").write_text(page)

    n_prod = 0
    for m in re.finditer(r"\{name:'([^']+)',kind:'([^']*)',category:'(\w+)',frame:'(\w+)',art:(\w+),price:(\d+),badge:'([^']*)'\}", content):
        name, kind_, cat, frame, art, price, badge = m.groups()
        img = arts.get(art, cover)
        desc = f"₹{price} · {kind_} · {frame} frame. Handmade to order by Quality Glass Emporium, Raebareli — doorstep pickup, WhatsApp order."
        stub(slugify(name), f"{name} — Quality Glass Emporium", desc, img, f"{SITE}/share/{slugify(name)}/")
        n_prod += 1
    n_cat = 0
    for m in re.finditer(r"\{id:'(\w+)',label:'([^']+)',summary:'([^']+)',art:(\w+)", content):
        cid, label, summary, art = m.groups()
        img = arts.get(art, cover)
        desc = f"{summary}. Explore the {label} collection at Quality Glass Emporium, Raebareli — from ₹699, WhatsApp order & doorstep pickup."
        stub("c-" + slugify(cid), f"{label} — Quality Glass Emporium", desc, img, f"{SITE}/share/c-{slugify(cid)}/", kind="website")
        n_cat += 1
    print(f"OG: {len(arts)} art images, {n_prod} product share pages, {n_cat} category share pages")

(output / "index.html").write_text(content)
# Basic CSP can be tightened once self-contained data: images and inline JS/CSS
# are replaced with separately built hashed assets.
(output / "_headers").write_text(
    "/*\n"
    "  X-Content-Type-Options: nosniff\n"
    "  Referrer-Policy: strict-origin-when-cross-origin\n"
    "  X-Frame-Options: DENY\n"
    "  Permissions-Policy: camera=(), microphone=(), geolocation=()\n"
    "  Cache-Control: no-store\n"
    + ("  X-Robots-Tag: noindex, nofollow\n" if app.name == "manager" else "")
)
print(f"Built {app.name}: {output / 'index.html'}")
