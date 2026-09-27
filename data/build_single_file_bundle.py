#!/usr/bin/env python3
"""Bundle every extracted table and archived page into one Markdown file."""
import csv
import json
from datetime import date
from pathlib import Path

DATA = Path(__file__).parent

def table(path, title):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return f"### {title}\n\n_No rows._\n"
    cols = list(rows[0])
    out = [f"### {title}\n", f"_{len(rows)} rows — source file `{path.name}`_\n",
           "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join((r.get(c) or "").replace("|", "\\|").replace("\n", " ") for c in cols) + " |")
    return "\n".join(out) + "\n"

parts = [
    "# All extracted data — single file", "",
    f"**Compiled:** {date.today().isoformat()}",
    "",
    "**Repository:** https://github.com/ancientgamer696-commits/quality",
    "",
    "**Companion files:** `data/README.md` (what each source is and its limits), `conversation/chat-log.md` (conversation record).", "",
    "Every figure below is a **dated research observation**, not a confirmed current price, stock level or approval. "
    "Old-site prices are the shop's own previous website; competitor rows are benchmark facts with one short quote each. "
    "Competitor images, artwork, reviews and full page copies are deliberately absent.", "",
    "## Contents", "",
    "1. Owner's own website — page inventory, products, categories, services, sizes, FAQ, journey, claims to verify",
    "2. Competitors — observations, page extracts, policy comparison",
    "3. Platform and requirements — free-tier limits, shop profile, feature requirements",
    "4. Raw archived text of all 51 owner-site pages",
    "", "---", "",
    "## 1. Owner's own website", "",
]
for name, title in [
    ("existing-site-pages.csv", "All publicly listed pages (51)"),
    ("existing-site-products.csv", "Product cards (32)"),
    ("existing-site-categories.csv", "Collections (10)"),
    ("existing-site-services.csv", "Services and old starting prices (8)"),
    ("existing-site-size-guide.csv", "Size-to-price anchors (6)"),
    ("existing-site-faq.csv", "FAQ answers"),
    ("existing-site-journey.csv", "Old four-step journey"),
    ("existing-site-claims-to-verify.csv", "Marketing claims needing evidence before reuse"),
]:
    parts.append(table(DATA / name, title))

parts += ["\n## 2. Competitors", ""]
for name, title in [
    ("competitor-observations.csv", "Flow, option and price observations"),
    ("competitor-pages-extract.csv", "Reviewed pages with structured facts and one short traceable quote each"),
    ("competitor-policies.csv", "Shipping, replacement, upload and payment comparison"),
]:
    parts.append(table(DATA / name, title))

parts += ["\n## 3. Platform and requirements", ""]
parts.append(table(DATA / "platform-limits.csv", "Free-tier limits with official sources"))
for name, title in [("shop-profile.json", "Shop profile"), ("feature-requirements.json", "Feature requirements")]:
    parts += [f"### {title}\n", f"_Source file `{name}`_\n", "```json",
              json.dumps(json.loads((DATA / name).read_text(encoding="utf-8")), ensure_ascii=False, indent=2), "```\n"]

parts += ["---", "", "## 4. Raw archived text of the owner's own pages", "",
          f"All {len(list((DATA / 'raw-pages').glob('*.txt')))} captured pages, verbatim visible text. "
          "Each block names its source URL and capture date. These are the owner's own pages, kept for migration.", ""]
for p in sorted((DATA / "raw-pages").glob("*.txt"), key=lambda x: x.name):
    parts += [f"### `{p.stem}`", "", f"_File `data/raw-pages/{p.name}`_", "", "```text", p.read_text(encoding="utf-8").rstrip("\n"), "```", ""]

out = DATA / "ALL-EXTRACTED-DATA.md"
out.write_text("\n".join(parts), encoding="utf-8")
print(f"{out.name}: {out.stat().st_size/1024:.0f} KB")
