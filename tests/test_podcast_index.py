import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import podcast_index  # noqa: E402


class RenderEpisodeTableTests(unittest.TestCase):
    def test_prefers_youtube_over_mp3(self):
        ep = {
            "number": 1,
            "title": "Sample",
            "release_date": "2026-01-01",
            "blurb": "Example blurb",
            "youtube_url": "https://youtube.example/watch?v=abc",
            "mp3_url": "https://audio.example/file.mp3",
            "discuss_url": "https://forum.example/topic",
        }

        html = podcast_index.render_episode_table(ep)

        self.assertIn('Listen on YouTube</a>', html)
        self.assertIn('https://youtube.example/watch?v=abc', html)
        self.assertNotIn('>mp3</a>', html)

    def test_falls_back_to_mp3_when_no_youtube(self):
        ep = {
            "number": 2,
            "title": "Sample",
            "release_date": "2026-01-02",
            "blurb": "Example blurb",
            "youtube_url": None,
            "mp3_url": "https://audio.example/file.mp3",
            "discuss_url": "https://forum.example/topic",
        }

        html = podcast_index.render_episode_table(ep)

        self.assertIn('<a href="https://audio.example/file.mp3">mp3</a>', html)
        self.assertNotIn('Listen on YouTube</a>', html)

    def test_falls_back_to_audio_when_no_media_urls(self):
        ep = {
            "number": 3,
            "title": "Sample",
            "release_date": "2026-01-03",
            "blurb": "Example blurb",
            "youtube_url": None,
            "mp3_url": None,
            "discuss_url": "https://forum.example/topic",
        }

        html = podcast_index.render_episode_table(ep)

        self.assertIn(" | audio | ", html)

    def test_escapes_title_blurb_and_date(self):
        ep = {
            "number": 4,
            "title": 'Tom & Jerry <Best> "Cuts"',
            "release_date": '2026-01-04 & beyond',
            "blurb": "Use <b>bold</b> & keep safe",
            "youtube_url": None,
            "mp3_url": None,
            "discuss_url": "https://forum.example/topic",
        }

        html = podcast_index.render_episode_table(ep)

        self.assertIn("Episode 4: Tom &amp; Jerry &lt;Best&gt; &quot;Cuts&quot;", html)
        self.assertIn("Posted by Reinhard on 2026-01-04 &amp; beyond", html)
        self.assertIn("Use &lt;b&gt;bold&lt;/b&gt; &amp; keep safe", html)
        self.assertNotIn("<b>bold</b>", html)

    def test_renders_focus_and_mention_tags(self):
        ep = {
            "number": 5,
            "title": "Tagged",
            "release_date": "2026-01-05",
            "blurb": "Example",
            "youtube_url": None,
            "mp3_url": None,
            "discuss_url": None,
            "systems": {
                "focus": ["shovelglove"],
                "mentions": ["no-s-diet"],
            },
        }
        systems = {
            "shovelglove": {
                "name": "Shovelglove",
                "group_label": "Body (output)",
                "color": "#2f6b43",
            },
            "no-s-diet": {
                "name": "No S Diet",
                "group_label": "Body (input)",
                "color": "#8f352d",
            },
        }

        html = podcast_index.render_episode_table(ep, systems)

        self.assertIn('system-tag--focus', html)
        self.assertIn('system-tag--mention', html)
        self.assertIn('title="Focus: Body (output)"', html)
        self.assertIn('title="Mentioned: Body (input)"', html)


class RenderIndexHtmlTests(unittest.TestCase):
    def test_renders_one_table_per_episode(self):
        episodes = [
            {
                "number": 10,
                "title": "First",
                "release_date": "2026-01-10",
                "blurb": "One",
                "youtube_url": None,
                "mp3_url": None,
                "discuss_url": None,
            },
            {
                "number": 9,
                "title": "Second",
                "release_date": "2026-01-09",
                "blurb": "Two",
                "youtube_url": None,
                "mp3_url": None,
                "discuss_url": None,
            },
        ]

        html = podcast_index.render_index_html(episodes)

        self.assertTrue(html.startswith(podcast_index.HEADER))
        self.assertTrue(html.endswith(podcast_index.FOOTER))
        self.assertEqual(html.count('<table border="0" cellpadding="2" cellspacing="0">'), 2)
        self.assertIn('<meta name="description"', html)
        self.assertIn('<link rel="canonical" href="https://podcast.everydaysystems.com/" />', html)


class RenderSitemapXmlTests(unittest.TestCase):
    def test_renders_root_table_and_episode_urls(self):
        episodes = [{"number": 10}, {"number": 9}]

        xml = podcast_index.render_sitemap_xml(episodes)

        self.assertTrue(xml.startswith('<?xml version="1.0" encoding="UTF-8"?>'))
        self.assertEqual(xml.count("<url><loc>"), 4)
        self.assertIn("<loc>https://podcast.everydaysystems.com/</loc>", xml)
        self.assertIn("<loc>https://podcast.everydaysystems.com/table/</loc>", xml)
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

    def test_system_colors_are_unique_and_groups_are_valid(self):
        group_ids = {group["id"] for group in self.catalog["groups"]}
        colors = [system["color"] for system in self.catalog["systems"]]
        self.assertEqual(len(colors), len(set(colors)))
        self.assertTrue(all(system["group"] in group_ids for system in self.catalog["systems"]))


if __name__ == "__main__":
    unittest.main()
