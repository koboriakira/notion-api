from unittest import TestCase

from notion_api.restaurant.domain.restaurant import Restaurant


class TestRestaurant(TestCase):
    def test_インスタンスの生成(self):
        # When
        actual = Restaurant.generate(
            title="店名",
            url="https://example.com",
            tag_relation=["abc123", "def456"],
        )

        # Then
        self.assertEqual(actual.name.text, "店名")
        self.assertEqual(actual.url.url, "https://example.com")
        self.assertEqual(2, len(actual.tags.id_list))
        self.assertIn("abc123", actual.tags.id_list)
        self.assertIn("def456", actual.tags.id_list)
