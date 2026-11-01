#!/usr/bin/env python3
"""Render branded 1200x630 Open Graph cards for every product & category.

Reads apps/shop/src/index.html (products + categories + embedded data-URI art),
writes apps/shop/src/og-pre/<slug>.jpg (+ c-<id>.jpg) and the favicon set
apps/shop/src/icon.png / apple-touch-icon.png. Requires Pillow.

Run after changing the catalog:  python3 scripts/make_og_cards.py
build.py prefers these pre-rendered cards and falls back to raw art if absent,
so CI (stdlib-only) keeps working either way.
"""
import base64
import io
import pathlib
import re

from PIL import Image, ImageDraw, ImageFont

root = pathlib.Path(__file__).resolve().parents[1]
src = root / "apps" / "shop" / "src"
fonts = root / "assets" / "fonts"
W, H = 1200, 630

html = (src / "index.html").read_text()


def data_uri(name):
    m = re.search(name + r"\s*=\s*'data:image/jpeg;base64,([^']+)'", html)
    return Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert("RGB") if m else None


ARTS = {n: data_uri(n) for n in ("HERO", "ANIME", "SACRED", "ABSTRACT", "ART")}

F_BRAND = ImageFont.truetype(str(fonts / "Cinzel.ttf"), 30)
F_TITLE = ImageFont.truetype(str(fonts / "Montserrat.ttf"), 58)
F_META = ImageFont.truetype(str(fonts / "Montserrat.ttf"), 32)
F_SUB = ImageFont.truetype(str(fonts / "Montserrat.ttf"), 23)

GOLD = (213, 176, 86)
WHITE = (241, 243, 249)
DIM = (196, 203, 219)
INK = (13, 16, 26)


def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)
    x = (img.width - w) // 2
    y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines[:3]


def card(bg_img, title, meta, sub, badge, out):
    scale = 1.5  # supersample then downscale = crisp text edges
    cw, ch = int(W * scale), int(H * scale)
    im = cover(bg_img, cw, ch)
    g = Image.new("L", (cw, ch))
    gd = ImageDraw.Draw(g)
    for x in range(cw):
        a = 236 if x < int(cw * 0.48) else max(0, int(236 - (x - cw * 0.48) * 236 / (cw * 0.38)))
        gd.line([(x, 0), (x, ch - 1)], fill=a)
    overlay = Image.new("RGB", (cw, ch), INK)
    im = Image.composite(overlay, im, g)
    d = ImageDraw.Draw(im)

    L, y = int(84 * scale), int(84 * scale)
    d.text((L, y), "QUALITY GLASS EMPORIUM", font=ImageFont.truetype(str(fonts / "Cinzel.ttf"), int(28 * scale)), fill=GOLD)
    d.rounded_rectangle([L, y + int(46 * scale), L + int(96 * scale), y + int(51 * scale)], 3, fill=GOLD)

    y += int(92 * scale)
    for ln in wrap(d, title, ImageFont.truetype(str(fonts / "Montserrat.ttf"), int(56 * scale)), int(cw * 0.56)):
        d.text((L, y), ln, font=ImageFont.truetype(str(fonts / "Montserrat.ttf"), int(56 * scale)), fill=WHITE)
        y += int(72 * scale)
    y += int(14 * scale)
    if meta:
        d.text((L, y), meta, font=ImageFont.truetype(str(fonts / "Montserrat.ttf"), int(30 * scale)), fill=GOLD)
        y += int(46 * scale)
    d.text((L, int(ch - 86 * scale)), sub, font=ImageFont.truetype(str(fonts / "Montserrat.ttf"), int(21 * scale)), fill=DIM,
           stroke_width=int(3 * scale), stroke_fill=(8, 10, 17))

    if badge:
        f = ImageFont.truetype(str(fonts / "Montserrat.ttf"), int(18 * scale))
        tw = d.textlength(badge, font=f)
        bx1 = cw - int(56 * scale)
        bx0 = bx1 - tw - int(34 * scale)
        d.rounded_rectangle([bx0, int(48 * scale), bx1, int(48 * scale) + int(44 * scale)], 22 * int(scale), fill=GOLD)
        d.text((bx0 + int(17 * scale), int(58 * scale)), badge, font=f, fill=INK)

    im = im.resize((W, H), Image.LANCZOS)
    im.save(out, quality=80, optimize=True)
    return out


out_dir = src / "og-pre"
out_dir.mkdir(exist_ok=True)

SUB = "Custom handmade frames · Raebareli · WhatsApp order & doorstep pickup"
n = 0
for m in re.finditer(r"\{name:'([^']+)',kind:'([^']*)',category:'(\w+)',frame:'(\w+)',art:(\w+),price:(\d+),badge:'([^']*)'\}", html):
    name, kind_, cat, frame, art, price, badge = m.groups()
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    bg = ARTS.get(art) or ARTS["HERO"]
    card(bg, name, f"₹{price}  ·  {frame} frame", SUB, badge.upper() if badge else "", out_dir / f"{slug}.jpg")
    n += 1

catmin = {}
for m in re.finditer(r"category:'(\w+)'[^}]*price:(\d+)", html):
    c, p = m.group(1), int(m.group(2))
    catmin[c] = min(catmin.get(c, 10**9), p)
for m in re.finditer(r"\{id:'(\w+)',label:'([^']+)',summary:'([^']+)',art:(\w+)", html):
    cid, label, summary, art = m.groups()
    bg = ARTS.get(art) or ARTS["HERO"]
    card(bg, label, f"From ₹{catmin.get(cid, 699)}", SUB, "", out_dir / f"c-{cid}.jpg")
    n += 1

# favicon + apple-touch from hero with brand overlay
hero = cover(ARTS["HERO"], 512, 512)
ov = Image.new("RGBA", (512, 512), (10, 12, 20, 120))
hero = Image.alpha_composite(hero.convert("RGBA"), ov)
d = ImageDraw.Draw(hero)
f = ImageFont.truetype(str(fonts / "Cinzel.ttf"), 150)
d.text((256, 250), "QG", font=f, fill=GOLD, anchor="mm")
hero.convert("RGB").save(src / "icon.png")
hero.resize((180, 180), Image.LANCZOS).convert("RGB").save(src / "apple-touch-icon.png")

sizes = [(p.name, p.stat().st_size) for p in sorted(out_dir.glob("*.jpg"))]
big = [s for s in sizes if s[1] > 300_000]
for s in sizes:
    print(f"  {s[0]:38s} {s[1]//1024:>4} KB")
print(f"rendered {n} cards; over-300KB: {len(big)}")
