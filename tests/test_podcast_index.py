import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import podcast_index  # noqa: E402


CATALOG = {
    "groups": [
        {"id": "body-input", "label": "Body (input)", "color": "#9b3a2a"},
        {"id": "body-output", "label": "Body (output)", "color": "#2f7040"},
    ],
    "systems": [
        {"id": "no-s-diet", "name": "No S Diet", "group": "body-input"},
        {"id": "shovelglove", "name": "Shovelglove", "group": "body-output"},
    ],
}

MINI_TEMPLATE = "<c><!--RESULTS_COUNT--></c><tbody><!--EPISODE_ROWS--></tbody><script id=\"d\"><!--PODCAST_DATA--></script>"


class RenderEpisodeRowTests(unittest.TestCase):
    def test_links_title_to_episode_page_only(self):
        ep = {
            "number": 1,
            "title": "Sample",
            "release_date": "2026-01-01",
            "blurb": "Example blurb",
            "youtube_url": "https://youtube.example/watch?v=abc",
            "mp3_url": "https://audio.example/file.mp3",
            "discuss_url": "https://forum.example/topic",
            "length_minutes": 12,
        }

        html = podcast_index.render_episode_row(ep)

        self.assertIn('<td class="episode-title"><a href="episode/1/">Sample</a></td>', html)
        self.assertNotIn("youtube.example", html)
        self.assertNotIn("forum.example", html)
        self.assertIn('<td class="episode-length">12</td>', html)

    def test_missing_fields_fall_back_to_placeholders(self):
        html = podcast_index.render_episode_row({"number": 2})

        self.assertIn('<a href="episode/2/">Episode 2</a>', html)
        self.assertIn('<td class="episode-date">—</td>', html)
        self.assertIn('<td class="episode-length">—</td>', html)

    def test_escapes_title_blurb_and_date(self):
        ep = {
            "number": 4,
            "title": 'Tom & Jerry <Best> "Cuts"',
            "release_date": '2026-01-04 & beyond',
            "blurb": "Use <b>bold</b> & keep safe",
        }

        html = podcast_index.render_episode_row(ep)

        self.assertIn('Tom &amp; Jerry &lt;Best&gt; &quot;Cuts&quot;', html)
        self.assertIn('2026-01-04 &amp; beyond', html)
        self.assertIn("Use &lt;b&gt;bold&lt;/b&gt; &amp; keep safe", html)
        self.assertNotIn("<b>bold</b>", html)

    def test_renders_focus_and_mention_tags_with_family_colors(self):
        ep = {"number": 5, "title": "Tagged", "systems": {"focus": ["shovelglove"], "mentions": ["no-s-diet"]}}

        html = podcast_index.render_episode_row(ep, podcast_index.enrich_systems(CATALOG))

        self.assertIn('class="system-tag focus" data-tag-system="shovelglove" style="--tag-color:#2f7040"', html)
        self.assertIn('class="system-tag mention" data-tag-system="no-s-diet" style="--tag-color:#9b3a2a"', html)
        self.assertIn('title="Focus · Body (output) family. Click to filter by this system."', html)
        self.assertIn('title="Mentioned · Body (input) family. Click to filter by this system."', html)

    def test_collapses_tags_beyond_the_visible_limit(self):
        ep = {"number": 6, "title": "Many", "systems": {"focus": ["shovelglove"], "mentions": ["no-s-diet"]}}

        html = podcast_index.render_episode_row(ep, podcast_index.enrich_systems(CATALOG))
        collapsed = podcast_index.render_system_tags(ep, podcast_index.enrich_systems(CATALOG), visible_limit=1)

        self.assertNotIn("more-tags", html)
        self.assertIn('<details class="more-tags"><summary>+1 more</summary>', collapsed)


class RenderIndexHtmlTests(unittest.TestCase):
    def test_renders_rows_count_and_inline_data_in_descending_order(self):
        episodes = [
            {"number": 9, "title": "Second", "release_date": "2026-01-09", "blurb": "Two"},
            {"number": 10, "title": "First", "release_date": "2026-01-10", "blurb": "One"},
        ]

        html = podcast_index.render_index_html(episodes, CATALOG, template=MINI_TEMPLATE)

        self.assertEqual(html.count("<tr>"), 2)
        self.assertLess(html.index("First"), html.index("Second"))
        self.assertIn("<c><strong>2</strong> episodes</c>", html)
        data = json.loads(re.search(r'<script id="d">(.*)</script>', html, re.S).group(1))
        self.assertEqual([ep["number"] for ep in data["episodes"]], [10, 9])
        self.assertEqual(data["systems"], CATALOG)

    def test_inline_data_cannot_close_the_script_block(self):
        episodes = [{"number": 1, "title": "Tricky </script><script>alert(1)</script>"}]

        html = podcast_index.render_index_html(episodes, CATALOG, template=MINI_TEMPLATE)

        payload = re.search(r'<script id="d">(.*)</script>', html, re.S).group(1)
        self.assertNotIn("</script>", payload)
        self.assertIn("<\\/script>", payload)
        self.assertEqual(json.loads(payload)["episodes"][0]["title"], episodes[0]["title"])

    def test_real_template_has_all_markers_and_page_metadata(self):
        html = podcast_index.render_index_html([{"number": 1, "title": "Only"}], CATALOG)

        self.assertIn('<link rel="canonical" href="https://podcast.everydaysystems.com/" />', html)
        self.assertIn('<meta name="description"', html)
        self.assertIn('<td class="episode-number">1</td>', html)
        for marker in (podcast_index.ROWS_MARKER, podcast_index.COUNT_MARKER, podcast_index.DATA_MARKER):
            self.assertNotIn(marker, html)

    def test_missing_marker_raises(self):
        with self.assertRaises(ValueError):
            podcast_index.render_index_html([], CATALOG, template="<p>no markers</p>")


class RenderSitemapXmlTests(unittest.TestCase):
    def test_renders_root_and_episode_urls(self):
        episodes = [{"number": 10}, {"number": 9}]

        xml = podcast_index.render_sitemap_xml(episodes)

        self.assertTrue(xml.startswith('<?xml version="1.0" encoding="UTF-8"?>'))
        self.assertEqual(xml.count("<url><loc>"), 3)
        self.assertIn("<loc>https://podcast.everydaysystems.com/</loc>", xml)
        self.assertNotIn("/table/", xml)
        self.assertIn("<loc>https://podcast.everydaysystems.com/episode/10/</loc>", xml)
        self.assertIn("<loc>https://podcast.everydaysystems.com/episode/9/</loc>", xml)


class MetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.episodes = json.loads((ROOT / "metadata" / "episodes.json").read_text())
        cls.catalog = json.loads((ROOT / "metadata" / "systems.json").read_text())

    def test_every_episode_has_a_known_positive_length(self):
        self.assertTrue(all(episode.get("length_minutes", 0) > 0 for episode in self.episodes))

    def test_episode_system_ids_are_valid_and_relationships_do_not_overlap(self):
        valid_ids = {system["id"] for system in self.catalog["systems"]}
        for episode in self.episodes:
            relationships = episode.get("systems", {})
            focus = relationships.get("focus", [])
            mentions = relationships.get("mentions", [])
            self.assertTrue(set(focus) <= valid_ids, episode["number"])
            self.assertTrue(set(mentions) <= valid_ids, episode["number"])
            self.assertFalse(set(focus) & set(mentions), episode["number"])
            self.assertEqual(len(focus), len(set(focus)), episode["number"])
            self.assertEqual(len(mentions), len(set(mentions)), episode["number"])

    def test_family_colors_are_unique_and_groups_are_valid(self):
        group_ids = {group["id"] for group in self.catalog["groups"]}
        colors = [group["color"] for group in self.catalog["groups"]]
        self.assertEqual(len(colors), len(set(colors)))
        self.assertTrue(all(re.fullmatch(r"#[0-9a-f]{6}", color) for color in colors))
        self.assertTrue(all(system["group"] in group_ids for system in self.catalog["systems"]))
        self.assertTrue(all("color" not in system for system in self.catalog["systems"]))


if __name__ == "__main__":
    unittest.main()
