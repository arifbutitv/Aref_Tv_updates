"""Rebuild the public wallpaper catalogue after adding/deleting JPEG photos."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
for name in ("photos", "photos2"):
    folder = ROOT / name
    index = folder / "index.json"
    previous = json.loads(index.read_text(encoding="utf-8")) if index.exists() else []
    files = {p.name for p in folder.glob("*.jpg")}
    invalid = sorted(f for f in files if not re.fullmatch(r"[A-Za-z0-9_-]+\.jpg", f))
    if invalid:
        raise SystemExit("Use Latin letters, digits, hyphens and underscores: " + ", ".join(invalid))
    # Keep the existing order/credits/brightness; append new names deterministically.
    result = [p for p in previous if p["f"] in files]
    known = {p["f"] for p in result}
    result += [{"f": f, "c": "", "d": 0.95} for f in sorted(files - known)]
    index.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Catalogue: {len(result)} photos")
