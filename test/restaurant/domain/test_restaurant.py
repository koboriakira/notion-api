from unittest import TestCase

from notion_api.restaurant.domain.restaurant import Restaurant


class TestRestaurant(TestCase):
    def test_インスタンスの生成(self):
        # When
        actual = Restaurant.create(
            title="店名",
            url="https://example.com",
            tag_relation=["abc123", "def456"],
        )

        # Then
        self.assertEqual(actual.restaurant_name, "店名")
        self.assertEqual(actual.restaurant_url, "https://example.com")
        self.assertEqual(2, len(actual.tag_relation))
        self.assertIn("abc123", actual.tag_relation)
        self.assertIn("def456", actual.tag_relation)
