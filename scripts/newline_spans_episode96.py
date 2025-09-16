#!/usr/bin/env python3
"""
Insert a newline before every '<span' in episode 96 HTML for readability.
"""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
target = root / 'episode' / '96' / 'index.html'

text = target.read_text(encoding='utf-8')
updated = text.replace('<span', '\n<span')

if updated != text:
    target.write_text(updated, encoding='utf-8')
    print('Updated newlines before <span in', target)
else:
    print('No changes made (nothing to update).')
