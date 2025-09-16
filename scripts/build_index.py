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
from html import escape

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / 'metadata' / 'episodes.json'
DEFAULT_OUT  = ROOT / 'index.html'

HEADER = """<!DOCTYPE html>
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Everyday Systems Podcast</title>
  <style type=\"text/css\">body { background-image: url(assets/images/random_grey_variations.png) } #main { padding: 7px; max-width:800px; margin-left: auto; margin-right: auto; background-image: url(assets/images/white_texture.png); border-radius: 11px; } h1,h2,h3 { font-family: Arial, Helvetica, Geneva, sans-serif; } h1 { font-size:125%; } h2 { font-size:110%; } h3 { font-size:100%; } .title { font-weight:bold; } .date { font-size:75%; }</style>
</head>
<body>
<div id=\"main\">
<h1><a href=\"/\">Everyday Systems</a>: Podcast [ <a href=\"http://reinhard.libsyn.com/rss\">rss</a> | <a href=\"https://podcasts.apple.com/us/podcast/everyday-systems-podcast/id188988881\">apple podcasts</a> | <a href=\"https://open.spotify.com/show/5ZSps0RuOWK3R1aCHpeeVZ\">spotify</a> | <a href=\"https://www.youtube.com/playlist?list=PLfC6J9cSGWC8PDkwb6KUWp_QShHr0S8SZ\">youtube</a>]</h1>
<p>On this page you'll find links to Everyday Systems Podcast audio, approximate transcripts,
 and bulletin board discussions.</p>
<p>Subscribe on  <a href=\"https://podcasts.apple.com/us/podcast/everyday-systems-podcast/id188988881\">Apple Podcasts</a>, <a href=\"https://open.spotify.com/show/5ZSps0RuOWK3R1aCHpeeVZ\">Spotify</a>, <a href=\"https://www.youtube.com/playlist?list=PLfC6J9cSGWC8PDkwb6KUWp_QShHr0S8SZ\">youtube</a>, or wherever you get your podcasts.</p>
"""

FOOTER = """
<p>By <a href=\"mailto:reinhard.engels@gmail.com\">Reinhard Engels</a></p>
<p>© 2002-2025  <a href=\"http://everydaysystems.com\">Everyday Systems LLC</a>, All Rights Reserved.</p>
</div><script src=\"/assets/js/year.js?v=2\" defer></script><script src=\"/assets/js/youtube-embeds.js\" defer></script>
</body>\n"""

def load_meta():
    data = json.loads(META.read_text())
    # ensure numeric sort
    data.sort(key=lambda e: e['number'], reverse=True)
    return data


def table_for(ep: dict) -> str:
    num = ep['number']
    title = ep.get('title') or f"Episode {num}"
    safe_title = escape(f"Episode {num}: {title}" if not title.startswith("Episode") else title)
    date = ep.get('release_date')
    date_html = f"Posted by Reinhard on {escape(date)}" if date else "&nbsp;"
    blurb = ep.get('blurb') or ''
    blurb_html = escape(blurb)
    # transcript link path assumed predictable
    transcript_href = f"./episode/{num}/"
    mp3_url = ep.get('mp3_url') or ''
    discuss_url = ep.get('discuss_url') or ''
    youtube_url = ep.get('youtube_url') or ''
    # Prefer youtube listening experience; fallback to mp3 if youtube missing.
    if youtube_url:
        listen_fragment = f'<a href="{youtube_url}">Listen on YouTube</a>'
    elif mp3_url:
        listen_fragment = f'<a href="{mp3_url}">mp3</a>'
    else:
        listen_fragment = 'audio'
    parts = [
        '<table border="0" cellpadding="2" cellspacing="0">',
        f'  <tr><td class="title">{safe_title}</td></tr>',
        f'  <tr><td class="date">{date_html}</td></tr>',
        f'  <tr><td class="content">{blurb_html}</td></tr>',
        '  <tr><td>' + ' | '.join([
            f'<a href="{transcript_href}">Transcript</a>',
            listen_fragment,
            f'<a href="{discuss_url}">Discuss</a>' if discuss_url else 'Discuss'
        ]) + '</td></tr>',
        '  <tr><td>&nbsp;</td></tr>',
        '</table>'
    ]
    return '\n'.join(parts)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build podcast index from metadata")
    parser.add_argument('--out', dest='out', help='Alternate output path (defaults to index.html)')
    args = parser.parse_args()
    out_path = Path(args.out).resolve() if args.out else DEFAULT_OUT
    episodes = load_meta()
    tables = [table_for(ep) for ep in episodes]
    out_path.write_text(HEADER + '\n'.join(tables) + '\n' + FOOTER)
    print(f"Wrote {out_path} with {len(episodes)} episodes.")

if __name__ == '__main__':
    main()
