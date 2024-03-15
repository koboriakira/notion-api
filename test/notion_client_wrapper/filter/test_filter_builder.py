from datetime import date
from unittest import TestCase

from notion_api.notion_client_wrapper.filter.condition.date_condition import DateCondition
from notion_api.notion_client_wrapper.filter.condition.number_condition import NumberCondition
from notion_api.notion_client_wrapper.filter.condition.or_condition import OrCondition as Or
from notion_api.notion_client_wrapper.filter.condition.string_condition import StringCondition
from notion_api.notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_api.notion_client_wrapper.properties.date import Date
from notion_api.notion_client_wrapper.properties.number import Number
from notion_api.notion_client_wrapper.properties.select import Select
from notion_api.notion_client_wrapper.properties.status import Status
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

    def test_ステータス(self):
        # Given
        status = Status.from_status_name(name="ステータス", status_name="Done")

        # When
        actual = FilterBuilder().add_condition(StringCondition.not_equal(status)).build()

        # Then
        expected = {
            "property": "ステータス",
            "status": {
                "does_not_equal": "Done"
            }
        }

        self.assertEqual(expected, actual)

    def test_セレクト(self):
        # Given
        status = Select(
            name="タスク種別",
            selected_name="ゴミ箱",
            selected_id="123"
        )

        # When
        actual = FilterBuilder().add_condition(StringCondition.not_equal(status)).build()

        # Then
        expected = {
            "property": "タスク種別",
            "select": {
                "does_not_equal": "ゴミ箱"
            }
        }

        self.assertEqual(expected, actual)

    def test_andとor条件を併用(self):
        # Given
        status = Select(name="タスク種別", selected_name="ゴミ箱", selected_id="123")
        start_date = Date.from_start_date(name="実施日", start_date=date.fromisoformat("2024-03-15"))
        status_todo = Status.from_status_name(name="ステータス", status_name="ToDo")
        status_in_progress = Status.from_status_name(name="ステータス", status_name="InProgress")

        # When
        filter_builder = FilterBuilder()
        filter_builder = filter_builder.add_condition(StringCondition.not_equal(status))
        filter_builder = filter_builder.add_condition(DateCondition.equal(start_date))
        filter_builder = filter_builder.add_condition(Or.create(StringCondition.equal(status_todo), StringCondition.equal(status_in_progress)))
        actual = filter_builder.build()

        import json
        print(json.dumps(actual, indent=2, ensure_ascii=False))

        # Then
        expected = {
            "and": [
                {
                    "property": "タスク種別",
                    "select": {"does_not_equal": "ゴミ箱"}
                },
                {
                    "property": "実施日",
                    "date": {"equals": "2024-03-15"}
                },
                {
                    "or": [
                        {
                            "property": "ステータス",
                            "status": {"equals": "ToDo"}
                        },
                        {
                            "property": "ステータス",
                            "status": {"equals": "InProgress"}
                        },
                    ]
                }
            ]
        }

        self.assertEqual(expected, actual)
