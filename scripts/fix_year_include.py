#!/usr/bin/env python3
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
html_files = list(root.rglob('*.html'))
pattern = re.compile(r"[\x00-\x1F]*\s*(<script[^>]*src=\"/assets/js/year.js[^>]*></script>)", re.IGNORECASE)
# Also match lines where src appears without a leading <script
pattern2 = re.compile(r"[\x00-\x1F]*\s*(src=\"/assets/js/year.js[^>]*></script>)", re.IGNORECASE)

fixed = 0
for f in html_files:
    s = f.read_text(encoding='utf-8')
    s_new = s
    # First, replace any control chars prefixing a proper script tag (rare)
    s_new = re.sub(r"[\x00-\x1F]+<script\s+", "<script ", s_new)
    # Replace occurrences where the line is missing the opening <script
    s_new = re.sub(r"[\x00-\x1F]*\s*src=\"/assets/js/year.js", "<script src=\"/assets/js/year.js", s_new)
    if s_new != s:
        f.write_text(s_new, encoding='utf-8')
        fixed += 1

print(f"Fixed {fixed} files")
