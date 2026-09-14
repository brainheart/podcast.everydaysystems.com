#!/usr/bin/env python3
"""Generate index.html and sitemap.xml from metadata/episodes.json.

Usage:
    python scripts/build_index.py [--out ALT_FILE]

The front page is the sortable, filterable episode table. It is rendered from
scripts/index_template.html with every episode row pre-rendered and the
episode/system metadata inlined, so it works without extra requests and is
fully crawlable. Run this after any change to metadata/episodes.json,
metadata/systems.json, or the template.
"""
from __future__ import annotations
import json
from pathlib import Path

from podcast_index import render_index_html, render_sitemap_xml

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / 'metadata' / 'episodes.json'
SYSTEMS_META = ROOT / 'metadata' / 'systems.json'
DEFAULT_OUT  = ROOT / 'index.html'
DEFAULT_SITEMAP = ROOT / 'sitemap.xml'

def load_meta():
    data = json.loads(META.read_text())
    # ensure numeric sort
    data.sort(key=lambda e: e['number'], reverse=True)
    return data


def load_system_catalog():
    return json.loads(SYSTEMS_META.read_text())


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build podcast index from metadata")
    parser.add_argument('--out', dest='out', help='Alternate output path (defaults to index.html)')
    args = parser.parse_args()
    out_path = Path(args.out).resolve() if args.out else DEFAULT_OUT
    episodes = load_meta()
    out_path.write_text(render_index_html(episodes, load_system_catalog()), encoding='utf-8')
    print(f"Wrote {out_path} with {len(episodes)} episodes.")
    if not args.out:
        DEFAULT_SITEMAP.write_text(render_sitemap_xml(episodes), encoding='utf-8')
        print(f"Wrote {DEFAULT_SITEMAP} with {len(episodes) + 1} URLs.")

if __name__ == '__main__':
    main()
