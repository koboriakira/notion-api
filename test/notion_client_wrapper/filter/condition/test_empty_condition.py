from unittest import TestCase

from notion_api.notion_client_wrapper.filter.condition.empty_condition import EmptyCondition
from notion_api.notion_client_wrapper.properties.relation import Relation


class TestEmptyCondition(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_リレーションが空である条件(self):
        # When
        condition = EmptyCondition.true(prop_name="Task List", prop_type=Relation.TYPE)

        # Then
        expected = {"property": "Task List", "relation": {"is_empty": True}}
        self.assertEqual(expected, condition.__dict__())

    def test_リレーションが空でない条件(self):
        # When
        condition = EmptyCondition.false(prop_name="Task List", prop_type=Relation.TYPE)

        # Then
        expected = {"property": "Task List", "relation": {"is_not_empty": True}}
        self.assertEqual(expected, condition.__dict__())
