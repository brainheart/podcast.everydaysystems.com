"""Render the podcast front page (a sortable, filterable episode table) and sitemap.

The page template lives in ``scripts/index_template.html``. The builder fills in
pre-rendered episode rows, so the full episode list is present in the static
HTML for search engines and readers without JavaScript, and inlines the episode
and system metadata so the page's filtering script needs no extra requests.
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

SITE_URL = "https://podcast.everydaysystems.com"
TEMPLATE_PATH = Path(__file__).resolve().parent / "index_template.html"

ROWS_MARKER = "<!--EPISODE_ROWS-->"
COUNT_MARKER = "<!--RESULTS_COUNT-->"
DATA_MARKER = "<!--PODCAST_DATA-->"

VISIBLE_TAG_LIMIT = 5


def _valid_color(color: str | None) -> str:
    return color if color and re.fullmatch(r"#[0-9a-fA-F]{6}", color) else "#666666"


def enrich_systems(system_catalog: dict) -> dict[str, dict]:
    """Return systems keyed by ID with their family's label and color attached."""
    groups_by_id = {group["id"]: group for group in system_catalog.get("groups", [])}
    systems_by_id: dict[str, dict] = {}
    for system in system_catalog.get("systems", []):
        group = groups_by_id.get(system.get("group"), {})
        enriched = dict(system)
        enriched["group_label"] = group.get("label", "")
        # Color belongs to the family (group); systems inherit it.
        enriched["color"] = _valid_color(group.get("color") or system.get("color"))
        systems_by_id[system["id"]] = enriched
    return systems_by_id


def render_system_tags(ep: dict, systems_by_id: dict[str, dict], visible_limit: int = VISIBLE_TAG_LIMIT) -> str:
    """Render an episode's system tags with the same markup the page script produces."""
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
        name = escape(system.get("name") or system_id)
        relation_label = "Focus" if relationship == "focus" else "Mentioned"
        title = escape(f"{relation_label} · {system.get('group_label', '')} family. Click to filter by this system.")
        return (
            f'<button type="button" class="system-tag {relationship}" '
            f'data-tag-system="{escape(system_id)}" style="--tag-color:{_valid_color(system.get("color"))}" '
            f'title="{title}" aria-pressed="false">{name}</button>'
        )

    rendered = [tag for tag in (render_tag(*tag) for tag in tagged) if tag]
    if not rendered:
        return ""

    visible = rendered[:visible_limit]
    hidden = rendered[visible_limit:]
    if hidden:
        visible.append(
            '<details class="more-tags">'
            f'<summary>+{len(hidden)} more</summary>'
            + "".join(hidden)
            + "</details>"
        )
    return '<div class="system-tags" aria-label="Episode systems">' + "".join(visible) + "</div>"


def render_episode_row(ep: dict, systems_by_id: dict[str, dict] | None = None) -> str:
    num = int(ep["number"])
    title = escape(ep.get("title") or f"Episode {num}")
    date = escape(ep.get("release_date") or "—")
    blurb = escape(ep.get("blurb") or "")
    length = ep.get("length_minutes") or ""
    return "\n".join([
        "        <tr>",
        f'          <td class="episode-number">{num}</td>',
        f'          <td class="episode-date">{date}</td>',
        f'          <td class="episode-title"><a href="episode/{num}/">{title}</a></td>',
        f'          <td class="episode-description">{blurb}{render_system_tags(ep, systems_by_id or {})}</td>',
        f'          <td class="episode-length">{length if length else "—"}</td>',
        "        </tr>",
    ])


def render_inline_data(episodes: list[dict], system_catalog: dict) -> str:
    payload = json.dumps({"episodes": episodes, "systems": system_catalog}, ensure_ascii=False, separators=(",", ":"))
    # Keep the JSON safe inside a <script> data block.
    return payload.replace("</", "<\\/")


def render_index_html(episodes: list[dict], system_catalog: dict | None = None, template: str | None = None) -> str:
    system_catalog = system_catalog or {"groups": [], "systems": []}
    systems_by_id = enrich_systems(system_catalog)
    ordered = sorted(episodes, key=lambda ep: int(ep["number"]), reverse=True)
    rows = "\n".join(render_episode_row(ep, systems_by_id) for ep in ordered)
    count = f"<strong>{len(ordered)}</strong> episodes"
    template = template if template is not None else TEMPLATE_PATH.read_text(encoding="utf-8")
    for marker in (ROWS_MARKER, COUNT_MARKER, DATA_MARKER):
        if marker not in template:
            raise ValueError(f"Template is missing {marker}")
    return (
        template
        .replace(ROWS_MARKER, rows)
        .replace(COUNT_MARKER, count)
        .replace(DATA_MARKER, render_inline_data(ordered, system_catalog))
    )


def render_sitemap_xml(episodes: list[dict]) -> str:
    urls = [
        f"{SITE_URL}/",
        *(f"{SITE_URL}/episode/{episode['number']}/" for episode in episodes),
    ]
    entries = "\n".join(f"  <url><loc>{escape(url)}</loc></url>" for url in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n"
    )
