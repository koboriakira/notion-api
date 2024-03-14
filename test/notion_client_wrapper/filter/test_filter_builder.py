from unittest import TestCase

from notion_api.notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_api.notion_client_wrapper.properties.url import Url


class TestFilterBuilder(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_シンプルな条件を作成する(self):
        # Given
        spotify_url = "https://open.spotify.com/track/6tPlPsvzSM74vRVn9O5v9K"
        url = Url.from_url(name="Spotify", url=spotify_url)

        # When
        actual = FilterBuilder().single_equal(url)

        # Then
        expected = {
          "property": "Spotify",
          "url": {
              "equals": spotify_url
          }
        }
        self.assertEqual(expected, actual)
