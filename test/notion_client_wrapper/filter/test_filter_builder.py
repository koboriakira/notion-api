from unittest import TestCase

from notion_api.notion_client_wrapper.filter.condition.number_condition import NumberCondition
from notion_api.notion_client_wrapper.filter.condition.string_condition import StringCondition
from notion_api.notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_api.notion_client_wrapper.properties.number import Number
from notion_api.notion_client_wrapper.properties.url import Url

# https://developers.notion.com/reference/post-database-query-filter

class TestFilterBuilder(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_シンプルな条件を作成する(self):
        # Given
        spotify_url = "https://open.spotify.com/track/6tPlPsvzSM74vRVn9O5v9K"
        url = Url.from_url(name="Spotify", url=spotify_url)

        # When
        actual = FilterBuilder().add_condition(StringCondition.equal(url)).build()
        print(actual)

        # Then
        expected = {
          "property": "Spotify",
          "url": {
              "equals": spotify_url
          }
        }
        self.assertEqual(expected, actual)

    def test_2つのand条件を作成する(self):
        # Given
        spotify_url = "https://open.spotify.com/track/6tPlPsvzSM74vRVn9O5v9K"
        url = Url.from_url(name="Spotify", url=spotify_url)
        number = Number.from_num(name="Number", value=1)

        # When
        actual = FilterBuilder().add_condition(StringCondition.equal(url)).add_condition(NumberCondition.equal(number)).build()

        # Then
        expected = {
            "and": [
                {
                    "property": "Spotify",
                    "url": {
                        "equals": spotify_url
                    }
                },
                {
                    "property": "Number",
                    "number": {
                        "equals": 1
                    }
                }
            ]
        }
        self.assertEqual(expected, actual)
