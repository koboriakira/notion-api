from unittest import TestCase

from notion_api.video.domain.video import Video


class TestVideo(TestCase):
    def test_インスタンスの生成(self):
        # When
        actual = Video.create(
            title="動画名",
            url="https://www.youtube.com/watch?v=Xj6YiZZagzc",
            tag_relation=["abc123", "def456"],
        )

        # Then
        self.assertEqual(actual.video_name, "動画名")
        self.assertEqual(actual.video_url, "https://www.youtube.com/watch?v=Xj6YiZZagzc")
        self.assertEqual(2, len(actual.tag_relation))
        self.assertIn("abc123", actual.tag_relation)
        self.assertIn("def456", actual.tag_relation)
        self.assertEqual(
            actual.embed_youtube_url,
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/Xj6YiZZagzc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
        )
