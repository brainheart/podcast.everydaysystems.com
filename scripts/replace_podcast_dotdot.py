#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = "https://everydaysystems.com/podcast/.."
REPLACEMENT = "/episode"

changed = 0
scanned = 0
for path in ROOT.rglob("*.html"):
    scanned += 1
    text = path.read_text(encoding="utf-8", errors="ignore")
    if TARGET in text:
        new_text = text.replace(TARGET, REPLACEMENT)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1

print(f"Replaced literal '{TARGET}' with '{REPLACEMENT}' in {changed} file(s) out of {scanned} scanned.")
