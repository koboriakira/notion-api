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
        self.assertEqual(actual.tag_relation.to_str_list(), ["abc123", "def456"])
