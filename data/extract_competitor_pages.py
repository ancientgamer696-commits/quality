#!/usr/bin/env python3
"""Extract structured competitor facts (no competitor images, no full page copies).

For each reviewed page the script stores: what the page is, the factual points
found in it, and at most one short quoted snippet for the record. Competitor
page text, artwork and customer reviews are deliberately NOT archived.
"""
import csv
import re
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

OBSERVED = "2026-09-27"
OUT = Path(__file__).parent
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; QualityGlassResearch/1.0)"}

PAGES = [
    ("OnlineFraming", "homepage", "https://onlineframing.in/"),
    ("OnlineFraming", "shipping policy", "https://onlineframing.in/pages/shipping-policy"),
    ("OnlineFraming", "refund policy", "https://onlineframing.in/pages/refund-policy"),
    ("Framebazaar", "FAQs", "https://framebazaar.com/pages/faqs"),
    ("Framebazaar", "shipping policy", "https://framebazaar.com/policies/shipping-policy"),
    ("Framebazaar", "refund policy", "https://framebazaar.com/policies/refund-policy"),
    ("Framebazaar", "product example", "https://framebazaar.com/products/osaka-frame"),
    ("Framing World", "FAQs", "https://framingworld.in/pages/faqs"),
    ("CanvasChamp", "framed prints", "https://www.canvaschamp.in/framed-prints"),
    ("VistaPrint", "photo with frame", "https://www.vistaprint.in/photo-gifts/photo-with-frame"),
    ("Framebridge", "how it works", "https://www.framebridge.com/pages/how-it-works"),
    ("Framebridge", "pricing", "https://www.framebridge.com/pages/pricing"),
    ("Framebridge", "return policy", "https://www.framebridge.com/pages/return-policy"),
]

TOPICS = {
    "turnaround": r"(?:\b\d+\s*(?:-\s*\d+\s*)?(?:business |working )?days?\b|within \d+ (?:days|hours)|same[- ]day)",
    "shipping charge": r"(?:free (?:shipping|delivery)|shipping (?:charges|fee|cost)|₹\s?\d+\s*(?:flat)? shipping)",
    "payment methods": r"(?:UPI|Google Pay|PhonePe|Paytm|net ?banking|credit card|debit card|COD|cash on delivery|PayPal|Apple Pay)",
    "size handling": r"(?:custom size|any size|upto \d+\s*(?:x|×)\s*\d+|\d+\s*(?:x|×)\s*\d+\s*(?:inch|in|cm))",
    "upload limit": r"(?:max(?:imum)? file size|up to \d+\s?MB|\d+\s?MB)",
}

def text_of(url):
    r = requests.get(url, timeout=25, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    main = soup.find("main") or soup.body or soup
    return re.sub(r"[ \t]+", " ", "\n".join(l.strip() for l in main.get_text("\n").split("\n") if l.strip()))

rows, policies = [], []
for site, kind, url in PAGES:
    try:
        text = text_of(url)
    except Exception as exc:  # keep the record honest when a page blocks us
        rows.append({"site": site, "page_kind": kind, "source_url": url, "status": "fetch failed",
                     "observed_date": OBSERVED, "facts": str(exc)[:120], "quote_snippet": ""})
        print("failed:", url, type(exc).__name__)
        continue
    facts = {}
    for topic, pattern in TOPICS.items():
        hits = [m.group(0).strip() for m in re.finditer(pattern, text, re.I)]
        facts[topic] = "; ".join(dict.fromkeys(hits))[:220]
    prices = sorted({int(p.replace(",", "")) for p in re.findall(r"(?:₹|Rs\.?)\s?([\d,]{3,})", text)})
    usd = sorted({int(p) for p in re.findall(r"\$\s?(\d{2,4})(?!\d)", text)})
    snippet = ""
    for pattern in TOPICS.values():
        m = re.search(pattern, text, re.I)
        if m:
            start = max(0, m.start() - 90)
            snippet = text[start:m.end() + 90].replace("\n", " ").strip()[:220]
            break
    rows.append({
        "site": site, "page_kind": kind, "source_url": url, "status": "ok",
        "observed_date": OBSERVED,
        "facts": " | ".join(f"{k}: {v}" for k, v in facts.items() if v),
        "rupee_prices_seen_inr": ", ".join(str(p) for p in prices[:12]),
        "usd_prices_seen": ", ".join(str(p) for p in usd[:12]),
        "quote_snippet_for_record": snippet,
        "reused_verbatim_on_new_site": "no",
    })

with (OUT / "competitor-pages-extract.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
print(f"competitor-pages-extract.csv: {len(rows)} pages (structured facts + one short snippet each, no page copies)")
