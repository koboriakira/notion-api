from unittest import TestCase

from notion_api.notion_client_wrapper.filter.condition.empty_condition import EmptyCondition
from notion_api.notion_client_wrapper.properties.relation import Relation


class TestEmptyCondition(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_リレーションが空である条件(self):
        # Given
        relation = Relation(name="Task List")

        # When
        condition = EmptyCondition.true(property=relation)

        # Then
        expected = {
          "property": "Task List",
          "relation": {
            "is_empty": True
          }
        }
        self.assertEqual(expected, condition.__dict__())
