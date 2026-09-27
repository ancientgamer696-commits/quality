#!/usr/bin/env python3
"""Copy one self-contained demo into a Cloudflare Pages output directory.

Using only Python stdlib means Pages can build immediately without npm installs.
The manager output is intentionally a DEMO, not a secure admin application.
"""
import pathlib
import shutil
import sys

root = pathlib.Path(__file__).resolve().parents[1]
if len(sys.argv) != 2 or sys.argv[1] not in {"shop", "manager"}:
    raise SystemExit("Usage: python3 scripts/build.py shop|manager")
app = root / "apps" / sys.argv[1]
source = app / "src" / "index.html"
output = app / "dist"
output.mkdir(parents=True, exist_ok=True)
content = source.read_text()
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
