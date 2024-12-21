from datetime import date
from unittest import TestCase

from notion_api.music.domain.song import Song


class TestSong(TestCase):
    def test_インスタンスの生成(self):
        # When
        actual = Song.create(
            title="マシュマロカカオステーション",
            artist="アップアップガールズ(プロレス),らく",
            spotify_url="https://open.spotify.com/track/6lC9dDRmwpKcVWmWy0GfmO?si=731d95eb095543ac",
            tag_relation=["abc123", "def456"],
            release_date=date.fromisoformat("2020-12-25"),
        )

        # Then
        self.assertEqual(actual.song_title, "マシュマロカカオステーション")
        self.assertEqual(actual.spotify_url, "https://open.spotify.com/track/6lC9dDRmwpKcVWmWy0GfmO")
        self.assertEqual(actual.artist, "アップアップガールズ(プロレス), らく")
        self.assertCountEqual(actual.tag_relation, ["abc123", "def456"])
        self.assertTrue("abc123" in actual.tag_relation)
        self.assertTrue("def456" in actual.tag_relation)
        self.assertEqual(actual.release_date, date.fromisoformat("2020-12-25"))
        self.assertEqual(actual.cover, None)
        self.assertEqual(actual.block_children, [])
        self.assertEqual(actual.spotify_track_id, "6lC9dDRmwpKcVWmWy0GfmO")
