#!/usr/bin/env python3
"""Rebuild the public-site snapshots. Run only when consciously refreshing research.

Uses the shop owner's previous public HTML. Does not download images or reviews.
No authentication or API credentials used. Explicitly not a live catalog import.
"""
import csv
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://quality-glass-website.vercel.app"
OUT = Path(__file__).parent
OBSERVED = "2026-09-27"

def page(path):
    response = requests.get(BASE + path, timeout=20, headers={"User-Agent":"QualityGlassResearch/1.0"})
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def inr(text):
    found = re.search(r"₹\s*([\d,]+)", text or "")
    return int(found.group(1).replace(",", "")) if found else ""

def write_csv(name, fields, rows):
    with (OUT / name).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

home = page("/")
shop = page("/shop")
categories = []
for a in home.select('a[href^="/shop?category="]'):
    link = urljoin(BASE, a.get("href", ""))
    slug = a.get("href", "").split("category=", 1)[-1]
    if slug and slug not in {r["slug"] for r in categories}:
        title = a.select_one("h3")
        tagline = a.select_one("h3 + p")
        categories.append({"slug": slug, "display_name": title.get_text(" ", strip=True) if title else slug, "old_site_tagline": tagline.get_text(" ", strip=True) if tagline else "", "source_url": link, "observed_date": OBSERVED, "owner_approved": "no"})
write_csv("existing-site-categories.csv", list(categories[0]), categories)

products = []
for a in shop.select("a.shop-card[href^='/product/']"):
    slug = a["href"].split("/product/", 1)[1]
    h = a.select_one("h3")
    pars = a.find_all("p")
    image = a.find("img")
    source_image_path = ""
    if image:
        from urllib.parse import parse_qs, urlparse
        raw = image.get("src", "")
        source_image_path = parse_qs(urlparse(raw).query).get("url", [raw])[0]
    prices = [inr(p.get_text(" ", strip=True)) for p in pars if "₹" in p.get_text()]
    products.append({
        "slug": slug,
        "name": h.get_text(" ", strip=True) if h else "",
        "short_description": pars[0].get_text(" ", strip=True) if pars else "",
        "observed_price_inr": prices[0] if prices else "",
        "observed_crossed_out_price_inr": prices[1] if len(prices)>1 else "",
        "old_site_image_path_reference_only": source_image_path,
        "source_url": urljoin(BASE, a["href"]),
        "observed_date": OBSERVED,
        "stock_verified": "no",
        "price_owner_approved": "no",
        "image_rights_checked": "no",
        "publish_as_product": "no",
    })
write_csv("existing-site-products.csv", list(products[0]), products)
print(f"Wrote {len(categories)} old-site category records and {len(products)} old-site product cards; no images downloaded.")
