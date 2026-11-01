#!/usr/bin/env python3
"""Copy one self-contained demo into a Cloudflare Pages output directory.

Using only Python stdlib means Pages can build immediately without npm installs.
The manager output is intentionally a DEMO, not a secure admin application.

Shop builds additionally get the full Open Graph / link-preview set:
  - site-level og: + twitter: meta + LocalBusiness JSON-LD injected into index.html
  - branded 1200x630 cards per product/category (scripts/make_og_cards.py output in
    apps/shop/src/og-pre/); falls back to extracted raw art when not pre-rendered
  - /share/<slug>/ stub pages so links on WhatsApp/Facebook/X/iMessage render a
    rich card with that exact product's photo, price and a tap-through to the shop
  - favicon / apple-touch-icon
"""
import base64
import html
import json
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
    content = content.replace(
        'data-go="checkout">Continue to checkout ↗</button>',
        'disabled title="Preview only; checkout is not yet connected">Checkout unavailable in public preview</button>',
    )
    assert "Checkout unavailable in public preview" in content
    content = content.replace(
        '· Interactive prototype · No live payments or uploads',
        '· Public preview · Checkout disabled · No live payments or uploads',
    )

    # ---------- embedded art -> real files (fallback + generic og) ----------
    ogdir = output / "og"
    ogdir.mkdir(exist_ok=True)
    arts = {}
    for name in ("HERO", "ANIME", "SACRED", "ABSTRACT", "ART"):
        m = re.search(name + r"\s*=\s*'data:image/jpeg;base64,([^']+)'", content)
        if m:
            raw = base64.b64decode(m.group(1))
            (ogdir / f"{name.lower()}.jpg").write_bytes(raw)
            arts[name] = f"{SITE}/og/{name.lower()}.jpg"

    pre = app / "src" / "og-pre"
    for f in (pre.glob("*.jpg") if pre.exists() else []):
        raw = f.read_bytes()
        if len(raw) > 700_000:
            raise SystemExit(f"og card {f.name} too heavy ({len(raw)} B); re-run make_og_cards.py")
        (ogdir / f.name).write_bytes(raw)

    (output / "og-cover.jpg").write_bytes((app / "src" / "og-cover.jpg").read_bytes())
    for icon in ("icon.png", "apple-touch-icon.png"):
        f = app / "src" / icon
        if f.exists():
            (output / icon).write_bytes(f.read_bytes())
    cover = f"{SITE}/og-cover.jpg"

    # ---------- head: site OG + twitter + JSON-LD + icons ----------
    ld = ('<script type="application/ld+json">'
          '{"@context":"https://schema.org","@type":"Store","name":"Quality Glass Emporium",'
          f'"description":{json.dumps(DESC)},"url":"{SITE}/","image":"{cover}",'
          '"address":{"@type":"PostalAddress","addressLocality":"Raebareli","addressRegion":"Uttar Pradesh","addressCountry":"IN"},'
          '"areaServed":"Raebareli","currenciesAccepted":"INR","priceRange":"₹699 - ₹1599",'
          '"openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":'
          '["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"09:30","closes":"20:00"}}'
          "</script>")
    icons = ""
    if (output / "icon.png").exists():
        icons = (f'<link rel="icon" type="image/png" href="{SITE}/icon.png">'
                 f'<link rel="apple-touch-icon" href="{SITE}/apple-touch-icon.png">')
    og_block = ld + icons + (
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

    def stub(pdir, title, desc, image, url, ld_json=None):
        d = output / "share" / pdir
        d.mkdir(parents=True, exist_ok=True)
        t, ds, im = html.escape(title, quote=True), html.escape(desc, quote=True), html.escape(image, quote=True)
        ld_s = f"<script type=\"application/ld+json\">{ld_json}</script>" if ld_json else ""
        page = (
            "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\">"
            f"<title>{html.escape(title)}</title>"
            '<meta name="robots" content="noindex">'
            '<meta property="og:type" content="product">'
            '<meta property="og:site_name" content="Quality Glass Emporium">'
            f'<meta property="og:url" content="{url}">'
            f'<meta property="og:title" content="{t}">'
            f'<meta property="og:description" content="{ds}">'
            f'<meta property="og:image" content="{im}">'
            '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta property="og:image:alt" content="{t}">'
            '<meta name="twitter:card" content="summary_large_image">'
            f'<meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{ds}">'
            f'<meta name="twitter:image" content="{im}">'
            f'<meta http-equiv="refresh" content="0;url={SITE}/">'
            f"</head><body style=\"font-family:system-ui;background:#f8f6f1;color:#41506b;padding:40px\">"
            f"{html.escape(title)} — opening shop…{ld_s}</body></html>"
        )
        (d / "index.html").write_text(page)

    n_prod = 0
    for m in re.finditer(r"\{name:'([^']+)',kind:'([^']*)',category:'(\w+)',frame:'(\w+)',art:(\w+),price:(\d+),badge:'([^']*)'\}", content):
        name, kind_, cat, frame, art, price, badge = m.groups()
        sl = slugify(name)
        if (output / "og" / f"{sl}.jpg").exists():
            img = f"{SITE}/og/{sl}.jpg"
        else:
            img = arts.get(art, cover)
        desc = f"₹{price} · {kind_} · {frame} frame. Handmade to order by Quality Glass Emporium, Raebareli — doorstep pickup, WhatsApp order."
        ldj = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": name,
                          "description": desc, "image": img, "brand": {"@type": "Brand", "name": "Quality Glass Emporium"},
                          "offers": {"@type": "Offer", "price": price, "priceCurrency": "INR",
                                     "availability": "https://schema.org/InStock", "url": f"{SITE}/"}}, ensure_ascii=False)
        stub(sl, f"{name} — Quality Glass Emporium", desc, img, f"{SITE}/share/{sl}/", ldj)
        n_prod += 1
    n_cat = 0
    for m in re.finditer(r"\{id:'(\w+)',label:'([^']+)',summary:'([^']+)',art:(\w+)", content):
        cid, label, summary, art = m.groups()
        sl = "c-" + slugify(cid)
        if (output / "og" / f"{sl}.jpg").exists():
            img = f"{SITE}/og/{sl}.jpg"
        elif (output / "og" / f"c-{cid}.jpg").exists():
            img = f"{SITE}/og/c-{cid}.jpg"
        else:
            img = arts.get(art, cover)
        desc = f"{summary}. Explore the {label} collection at Quality Glass Emporium, Raebareli — from ₹699, WhatsApp order & doorstep pickup."
        stub(sl, f"{label} — Quality Glass Emporium", desc, img, f"{SITE}/share/{sl}/")
        n_cat += 1
    print(f"OG: {len(arts)} art, {n_prod} product + {n_cat} category share pages, "
          f"{len(list(ogdir.glob('*.jpg')))} images")

(output / "index.html").write_text(content)
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
