from __future__ import annotations

from html import escape
import re

SITE_URL = "https://podcast.everydaysystems.com"

HEADER = """<!DOCTYPE html>
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Everyday Systems Podcast</title>
  <meta name=\"description\" content=\"Episodes, transcripts, audio, and discussion links for the Everyday Systems Podcast by Reinhard Engels.\" />
  <link rel=\"canonical\" href=\"https://podcast.everydaysystems.com/\" />
  <style type=\"text/css\">
    body { background-image: url(assets/images/random_grey_variations.png) }
    #main { padding: 7px; max-width:800px; margin-left: auto; margin-right: auto; background-image: url(assets/images/white_texture.png); border-radius: 11px; }
    h1,h2,h3 { font-family: Arial, Helvetica, Geneva, sans-serif; }
    h1 { font-size:125%; }
    h2 { font-size:110%; }
    h3 { font-size:100%; }
    .title { font-weight:bold; }
    .date { font-size:75%; }
    .system-key { color:#555; font:75% Arial, Helvetica, sans-serif; margin-top:-.35rem; }
    .system-tags { display:flex; flex-wrap:wrap; gap:4px; align-items:center; margin-top:6px; font:11px Arial, Helvetica, sans-serif; }
    .system-tag { --tag-color:#666; display:inline-block; border:1px solid var(--tag-color); border-radius:999px; padding:2px 7px; line-height:1.25; white-space:nowrap; }
    .system-tag--focus { color:#fff; background:var(--tag-color); font-weight:bold; }
    .system-tag--mention { color:var(--tag-color); background:#fff; }
    .system-tags-more { display:inline; }
    .system-tags-more summary { display:inline-block; color:#555; cursor:pointer; list-style:none; border-bottom:1px dotted #777; }
    .system-tags-more summary::-webkit-details-marker { display:none; }
    .system-tags-more[open] { display:flex; flex-basis:100%; flex-wrap:wrap; gap:4px; }
    .system-tags-more[open] summary { flex-basis:100%; width:max-content; }
  </style>
</head>
<body>
<div id=\"main\">
<h1><a href=\"https://everydaysystems.com\">Everyday Systems</a>: Podcast [ <a href=\"http://reinhard.libsyn.com/rss\">rss</a> | <a href=\"https://podcasts.apple.com/us/podcast/everyday-systems-podcast/id188988881\">apple podcasts</a> | <a href=\"https://open.spotify.com/show/5ZSps0RuOWK3R1aCHpeeVZ\">spotify</a> | <a href=\"https://www.youtube.com/playlist?list=PLfC6J9cSGWC8PDkwb6KUWp_QShHr0S8SZ\">youtube</a>]</h1>
<p>On this page you'll find links to Everyday Systems Podcast audio, approximate transcripts,
 and bulletin board discussions.</p>
<p>Subscribe on  <a href=\"https://podcasts.apple.com/us/podcast/everyday-systems-podcast/id188988881\">Apple Podcasts</a>, <a href=\"https://open.spotify.com/show/5ZSps0RuOWK3R1aCHpeeVZ\">Spotify</a>, <a href=\"https://www.youtube.com/playlist?list=PLfC6J9cSGWC8PDkwb6KUWp_QShHr0S8SZ\">youtube</a>, or wherever you get your podcasts.</p>
<p class=\"system-key\">System tags: <strong>filled</strong> means a focus of the episode; outlined means meaningfully mentioned.</p>
"""

FOOTER = """
<p>By <a href=\"mailto:reinhard.engels@gmail.com\">Reinhard Engels</a></p>
<p>© 2002-2025  Reinhard Engels, All Rights Reserved.</p>
</div><script src=\"/assets/js/year.js?v=2\" defer></script><script src=\"/assets/js/youtube-embeds.js\" defer></script>
</body>\n"""


def render_system_tags(ep: dict, systems_by_id: dict[str, dict], visible_limit: int = 5) -> str:
    relationships = ep.get("systems") or {}
    tagged = [
        (system_id, "focus") for system_id in relationships.get("focus", [])
    ] + [
        (system_id, "mention") for system_id in relationships.get("mentions", [])
    ]

    def render_tag(system_id: str, relationship: str) -> str:
        system = systems_by_id.get(system_id)
        if not system:
            return ""
        color = system.get("color", "#666666")
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
            color = "#666666"
        name = escape(system.get("name") or system_id)
        relation_label = "Focus" if relationship == "focus" else "Mentioned"
        title = escape(f"{relation_label}: {system.get('group_label', '')}")
        return (
            f'<span class="system-tag system-tag--{relationship}" '
            f'style="--tag-color:{color}" title="{title}">{name}</span>'
        )

    rendered = [render_tag(*tag) for tag in tagged]
    rendered = [tag for tag in rendered if tag]
    if not rendered:
        return ""

    visible = rendered[:visible_limit]
    hidden = rendered[visible_limit:]
    if hidden:
        visible.append(
            '<details class="system-tags-more">'
            f'<summary>+{len(hidden)} more</summary>'
            + "".join(hidden)
            + "</details>"
        )
    return '<div class="system-tags" aria-label="Episode systems">' + "".join(visible) + "</div>"


def render_episode_table(ep: dict, systems_by_id: dict[str, dict] | None = None) -> str:
    num = ep["number"]
    title = ep.get("title") or f"Episode {num}"
    safe_title = escape(f"Episode {num}: {title}" if not title.startswith("Episode") else title)
    date = ep.get("release_date")
    date_html = f"Posted by Reinhard on {escape(date)}" if date else "&nbsp;"
    blurb = ep.get("blurb") or ""
    blurb_html = escape(blurb)
    tags_html = render_system_tags(ep, systems_by_id or {})
    transcript_href = f"./episode/{num}/"
    mp3_url = ep.get("mp3_url") or ""
    discuss_url = ep.get("discuss_url") or ""
    youtube_url = ep.get("youtube_url") or ""

    # Prefer youtube listening experience; fallback to mp3 if youtube missing.
    if youtube_url:
        listen_fragment = f'<a href="{youtube_url}">Listen on YouTube</a>'
    elif mp3_url:
        listen_fragment = f'<a href="{mp3_url}">mp3</a>'
    else:
        listen_fragment = "audio"

    parts = [
        '<table border="0" cellpadding="2" cellspacing="0">',
        f'  <tr><td class="title">{safe_title}</td></tr>',
        f'  <tr><td class="date">{date_html}</td></tr>',
        f'  <tr><td class="content">{blurb_html}{tags_html}</td></tr>',
        "  <tr><td>"
        + " | ".join(
            [
                f'<a href="{transcript_href}">Transcript</a>',
                listen_fragment,
                f'<a href="{discuss_url}">Discuss</a>' if discuss_url else "Discuss",
            ]
        )
        + "</td></tr>",
        "  <tr><td>&nbsp;</td></tr>",
        "</table>",
    ]
    return "\n".join(parts)


def render_index_html(episodes: list[dict], system_catalog: dict | None = None) -> str:
    system_catalog = system_catalog or {"groups": [], "systems": []}
    groups_by_id = {group["id"]: group for group in system_catalog.get("groups", [])}
    systems_by_id = {}
    for system in system_catalog.get("systems", []):
        enriched = dict(system)
        enriched["group_label"] = groups_by_id.get(system.get("group"), {}).get("label", "")
        systems_by_id[system["id"]] = enriched
    tables = [render_episode_table(ep, systems_by_id) for ep in episodes]
    return HEADER + "\n".join(tables) + "\n" + FOOTER


def render_sitemap_xml(episodes: list[dict]) -> str:
    urls = [
        f"{SITE_URL}/",
        f"{SITE_URL}/table/",
        *(f"{SITE_URL}/episode/{episode['number']}/" for episode in episodes),
    ]
    entries = "\n".join(f"  <url><loc>{escape(url)}</loc></url>" for url in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n"
    )
