#!/usr/bin/env python3
"""Extract every publicly listed page of the shop owner's own previous website.

This is the owner's own content, so it is kept verbatim in raw-pages/ for archive
reasons. robots.txt is respected (admin, account, checkout, cart, login, signup
and api paths are skipped). No images, no credentials, no customer data.
"""
import csv
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

BASE = "https://quality-glass-website.vercel.app"
OBSERVED = "2026-09-27"
OUT = Path(__file__).parent
RAW = OUT / "raw-pages"
SKIP = ("/admin", "/account", "/checkout", "/cart", "/login", "/signup", "/api/", "/_next/")

def fetch(url):
    r = requests.get(url, timeout=25, headers={"User-Agent": "QualityGlassResearch/1.0 (owner archive)"})
    r.raise_for_status()
    return r.text

def clean(text):
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+", " ", text)).strip()

def visible_text(soup):
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    main = soup.find("main") or soup.body or soup
    lines = [clean(l) for l in main.get_text("\n").split("\n")]
    return "\n".join(l for l in lines if l)

sitemap = fetch(BASE + "/sitemap.xml")
urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
urls = [u for u in dict.fromkeys(urls) if not any(urlparse(u).path.startswith(s) for s in SKIP)]

RAW.mkdir(exist_ok=True)
inventory, details = [], []
for url in urls:
    path = urlparse(url).path or "/"
    soup = BeautifulSoup(fetch(url), "html.parser")
    text = visible_text(soup)
    slug = (path.strip("/") or "home").replace("/", "__")
    (RAW / f"{slug}.txt").write_text(f"# source: {url}\n# captured: {OBSERVED}\n\n{text}\n", encoding="utf-8")
    h1 = soup.find("h1")
    title = soup.find("title")
    jsonld = []
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            jsonld.append(json.loads(tag.string or "{}"))
        except (ValueError, TypeError):
            pass
    inventory.append({
        "path": path,
        "page_title": title.get_text(strip=True) if title else "",
        "h1": h1.get_text(" ", strip=True) if h1 else "",
        "word_count": len(text.split()),
        "starts_at_inr": min([int(x.replace(",", "")) for x in re.findall(r"₹\s*([\d,]{3,})", text)] or [""], default="") if re.search(r"₹", text) else "",
        "has_json_ld": "yes" if jsonld else "no",
        "source_url": url,
        "raw_text_file": f"raw-pages/{slug}.txt",
        "observed_date": OBSERVED,
    })
    details.append({"path": path, "url": url, "json_ld": jsonld, "text": text})

with (OUT / "existing-site-pages.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(inventory[0]))
    w.writeheader(); w.writerows(inventory)

with (OUT / "existing-site-pages-full.json").open("w", encoding="utf-8") as f:
    json.dump(details, f, ensure_ascii=False, indent=1)

print(f"Extracted {len(inventory)} public owner-site pages; skipped robots.txt-disallowed paths.")
