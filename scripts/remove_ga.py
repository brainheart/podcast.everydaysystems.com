#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Patterns to remove
RE_URCHIN_TAG = re.compile(r"<script[^>]*src=[\"'][^\"']*urchin\.js[\"'][^>]*>\s*</script>\s*", re.I | re.S)
RE_URCHIN_TRACKER_LINE = re.compile(r"^\s*urchinTracker\(\);\s*$", re.M)
RE_UUACCT_LINE = re.compile(r"^\s*_uacct\s*=\s*[\"'][^\"']+[\"'];\s*$", re.M)
RE_NOSCRIPT_GTM = re.compile(r"<noscript>.*?googletagmanager\.com.*?</noscript>\s*", re.I | re.S)

GA_TOKENS = (
    "google-analytics.com",
    "googletagmanager.com",
    "gtag(",
    "analytics.js",
    "GTM-",
)

SCRIPT_BLOCK_RE = re.compile(r"<script\b.*?</script>", re.I | re.S)


def strip_ga_from_html(text: str) -> str:
    original = text
    # Remove explicit legacy bits first
    text = RE_URCHIN_TAG.sub("", text)
    text = RE_URCHIN_TRACKER_LINE.sub("", text)
    text = RE_UUACCT_LINE.sub("", text)
    text = RE_NOSCRIPT_GTM.sub("", text)

    # Remove any <script> blocks containing GA/GTM tokens
    def filter_script(match: re.Match) -> str:
        block = match.group(0)
        lowered = block.lower()
        if any(tok.lower() in lowered for tok in GA_TOKENS):
            return ""  # drop this script entirely
        return block

    text = SCRIPT_BLOCK_RE.sub(filter_script, text)
    return text


def process_file(path: Path) -> bool:
    content = path.read_text(encoding="utf-8", errors="ignore")
    new_content = strip_ga_from_html(content)
    if new_content != content:
        path.write_text(new_content, encoding="utf-8")
        return True
    return False


def main():
    changed = 0
    files = list(ROOT.rglob("*.html"))
    for f in files:
        try:
            if process_file(f):
                changed += 1
        except Exception as e:
            print(f"WARN: failed to process {f}: {e}")
    print(f"GA/GTM stripped in {changed} file(s) out of {len(files)} scanned.")

if __name__ == "__main__":
    main()
