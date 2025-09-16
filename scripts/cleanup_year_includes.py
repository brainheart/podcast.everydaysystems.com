#!/usr/bin/env python3
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
html_files = list(root.rglob('*.html'))
fixed = 0
for f in html_files:
    s = f.read_text(encoding='utf-8')
    s_new = s
    # Remove U+0001 if present
    if '\x01' in s_new:
        s_new = s_new.replace('\x01', '')
    # Collapse accidental duplicate script tokens
    if '<script<script' in s_new:
        s_new = s_new.replace('<script<script', '<script')
    # Also fix occurrences like '</div><script<script' etc
    if s_new != s:
        f.write_text(s_new, encoding='utf-8')
        fixed += 1
print(f'Cleaned {fixed} files')
