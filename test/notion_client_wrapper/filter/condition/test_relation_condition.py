from unittest import TestCase

from lotion.filter.condition import RelationCondition
from lotion.properties import Relation


class TestRelationCondition(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_contains(self):
        # When
        relation = Relation.from_id_list(name="プロジェクト", id_list=["5673db2d520f48fbad6622a38cf2ecad"])
        condition = RelationCondition.contains(relation)

        # Then
        expected = {"or": [{"property": "プロジェクト", "relation": {"contains": "5673db2d520f48fbad6622a38cf2ecad"}}]}
        self.assertEqual(expected, condition.__dict__())
