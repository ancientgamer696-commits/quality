from pathlib import Path
import subprocess
root = Path(__file__).resolve().parents[1]
for app in ("shop", "manager"):
    subprocess.run(["python3", str(root / "scripts" / "build.py"), app], check=True)
    source = (root / "apps" / app / "src" / "index.html").read_bytes()
    built = (root / "apps" / app / "dist" / "index.html").read_bytes()
    if app == "manager":
        assert source == built, f"{app} output differs from source"
    else:
        assert b"Checkout unavailable in public preview" in built
        assert b"data-go=\"checkout\">Continue to checkout" not in built
    assert b"Quality Glass Emporium" in built
print("Two Pages output directories pass smoke checks.")
