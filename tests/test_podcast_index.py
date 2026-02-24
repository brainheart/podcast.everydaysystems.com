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


if __name__ == "__main__":
    unittest.main()
