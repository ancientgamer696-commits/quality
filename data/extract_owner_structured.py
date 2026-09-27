#!/usr/bin/env python3
"""Structure the owner-site facts out of raw-pages/ (no network calls).

Every row keeps the page it came from and is marked whether the owner must
re-confirm it before it can appear on the new site.
"""
import csv
import re
from datetime import date
from pathlib import Path

OBSERVED = "2026-09-27"
OUT = Path(__file__).parent
RAW = OUT / "raw-pages"
BASE = "https://quality-glass-website.vercel.app"

def lines(name):
    return RAW.joinpath(name).read_text(encoding="utf-8").splitlines()

def csvout(name, rows):
    with (OUT / name).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"{name}: {len(rows)} rows")

# --- services: name / Hindi name / description / price basis -------------------
# Card layout in the captured text is:
#   name / Hindi name / English description / Hindi description / price / arrow
s = lines("services.txt")
services = []
for i, line in enumerate(s):
    if re.fullmatch(r"from ₹[\d,]+|quote by size|custom quote", line.strip()) and i >= 4:
        services.append({
            "service": s[i - 4].strip(),
            "service_hindi": s[i - 3].strip(),
            "description": s[i - 2].strip(),
            "description_hindi": s[i - 1].strip(),
            "price_basis_old_site": line.strip(),
            "includes_claimed": "frame + glass + mount + finishing (old-site claim)",
            "source_url": BASE + "/services",
            "observed_date": OBSERVED,
            "owner_reconfirm_before_publish": "yes",
        })
csvout("existing-site-services.csv", services)

# --- size guide from the home page -------------------------------------------
h = lines("home.txt")
sizes, tags = [], {"Photo", "Certificate", "Frame", "Poster", "Mirror", "Wedding"}
for i, line in enumerate(h):
    m = re.fullmatch(r"([0-9]+×[0-9]+|A[0-9])", line.strip())
    if m and i + 2 < len(h) and h[i + 1].strip() in tags and h[i + 2].strip().startswith("₹"):
        sizes.append({
            "size": m.group(1),
            "use_case": h[i + 1].strip(),
            "old_site_from_price_inr": int(h[i + 2].strip().replace("₹", "").replace(",", "")),
            "source_url": BASE + "/",
            "observed_date": OBSERVED,
            "owner_reconfirm_before_publish": "yes",
        })
csvout("existing-site-size-guide.csv", sizes)

# --- FAQ ----------------------------------------------------------------------
f = lines("faq.txt")
faq, category = [], ""
for i, line in enumerate(f):
    t = line.strip()
    if t in {"Products", "Shipping", "Returns", "Payments", "Services"}:
        category = t
    elif t.endswith("?") and i + 1 < len(f) and t != "Still have questions?":
        faq.append({
            "category": category,
            "question": t,
            "answer": f[i + 1].strip(),
            "source_url": BASE + "/faq",
            "observed_date": OBSERVED,
            "answer_owner_approved": "no",
        })
csvout("existing-site-faq.csv", faq)

# --- four-step journey --------------------------------------------------------
start = h.index("From phone to frame, in four steps.")
end = h.index("Reviews") if "Reviews" in h else len(h)
h = h[start:end]
journey, order = [], 0
for i, line in enumerate(h):
    if re.fullmatch(r"0[1-4]", line.strip()) and i + 2 < len(h):
        order += 1
        journey.append({
            "step": order,
            "title": h[i + 1].strip(),
            "detail": h[i + 2].strip(),
            "source_url": BASE + "/",
            "observed_date": OBSERVED,
        })
csvout("existing-site-journey.csv", journey)

# --- marketing claims that need evidence before reuse ------------------------
claims = [
    ("Justdial rating shown on old site", "4.9 / 5", "home", "Public listing snapshot; verify count and date on Justdial."),
    ("Order tracking without login", "Order number + phone number", "track", "Depends on real backend; not implemented."),
    ("Delivery area", "anywhere in Raebareli", "home/services", "Distance, charges and timeline unverified."),
    ("Same-day delivery mentioned in a testimonial", "same day", "home", "Customer-generated text; needs owner confirmation if reused."),
    ("No hidden charges", "frame, glass, mount and finishing included", "services", "Owner must confirm what each price includes."),
    ("Unlimited free photo upload", "studio uploader", "studio", "Storage/retention policy undefined."),
    ("10 to 200 piece bulk pricing", "special bulk pricing on WhatsApp", "bulk", "No published bulk rate card; quote manually."),
]
csvout("existing-site-claims-to-verify.csv", [{
    "claim": c, "old_site_value": v, "page": p, "verification_note": n,
    "source_url": f"{BASE}/{'' if p == 'home' else p}", "observed_date": OBSERVED,
} for c, v, p, n in claims])
