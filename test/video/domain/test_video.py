from unittest import TestCase

from notion_databases.video import Video


class TestVideo(TestCase):
    def test_インスタンスの生成(self):
        # When
        actual = Video.generate(
            title="動画名",
            url="https://www.youtube.com/watch?v=Xj6YiZZagzc",
            tag_relation=["abc123", "def456"],
        )

        # Then
        self.assertEqual(actual.title.text, "動画名")
        self.assertEqual(actual.url.url, "https://www.youtube.com/watch?v=Xj6YiZZagzc")
        self.assertEqual(2, len(actual.tags.id_list))
        self.assertIn("abc123", actual.tags.id_list)
        self.assertIn("def456", actual.tags.id_list)
        self.assertEqual(
            actual.embed_youtube_url,
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/Xj6YiZZagzc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
        )
