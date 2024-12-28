from unittest import TestCase

from notion_databases.zettlekasten import Zettlekasten


class TestZettlekasten(TestCase):
    def test_インスタンスの生成(self):
        # When
        actual = Zettlekasten.generate(
            title="Zettlekastenタイトル",
            reference_url="https://www.youtube.com/watch?v=Xj6YiZZagzc",
            tag_relation=["abc123", "def456"],
        )

        # Then
        self.assertEqual(actual.title.text, "Zettlekastenタイトル")
        self.assertEqual(actual.reference_url.url, "https://www.youtube.com/watch?v=Xj6YiZZagzc")
        self.assertEqual(2, len(actual.tags.id_list))
        self.assertIn("abc123", actual.tags.id_list)
        self.assertIn("def456", actual.tags.id_list)
