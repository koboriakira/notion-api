from unittest import TestCase

from notion_api.zettlekasten.domain.zettlekasten import Zettlekasten


class TestZettlekasten(TestCase):
    def test_インスタンスの生成(self):
        # When
        actual = Zettlekasten.create(
            title="Zettlekastenタイトル",
            reference_url="https://www.youtube.com/watch?v=Xj6YiZZagzc",
            tag_relation=["abc123", "def456"],
        )

        # Then
        self.assertEqual(actual.zettlekasten_name, "Zettlekastenタイトル")
        self.assertEqual(actual.reference_url, "https://www.youtube.com/watch?v=Xj6YiZZagzc")
        self.assertEqual(2, len(actual.tag_relation))
        self.assertIn("abc123", actual.tag_relation)
        self.assertIn("def456", actual.tag_relation)
