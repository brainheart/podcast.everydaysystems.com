#!/usr/bin/env python3
"""Generate index.html from metadata/episodes.json.

Usage:
    python scripts/build_index.py [--out ALT_FILE]

It will read episodes.json, sort episodes descending by number, and emit a static
HTML file with the same header/footer as the existing index, but prettified.

Null fields (title, release_date, blurb) will fall back to placeholders derived
from existing episode page filenames or left blank if not available.
"""
from __future__ import annotations
import json
from pathlib import Path

from podcast_index import render_index_html, render_sitemap_xml

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / 'metadata' / 'episodes.json'
DEFAULT_OUT  = ROOT / 'index.html'
DEFAULT_SITEMAP = ROOT / 'sitemap.xml'

def load_meta():
    data = json.loads(META.read_text())
    # ensure numeric sort
    data.sort(key=lambda e: e['number'], reverse=True)
    return data


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build podcast index from metadata")
    parser.add_argument('--out', dest='out', help='Alternate output path (defaults to index.html)')
    args = parser.parse_args()
    out_path = Path(args.out).resolve() if args.out else DEFAULT_OUT
    episodes = load_meta()
    out_path.write_text(render_index_html(episodes), encoding='utf-8')
    print(f"Wrote {out_path} with {len(episodes)} episodes.")
    if not args.out:
        DEFAULT_SITEMAP.write_text(render_sitemap_xml(episodes), encoding='utf-8')
        print(f"Wrote {DEFAULT_SITEMAP} with {len(episodes) + 2} URLs.")

if __name__ == '__main__':
    main()
