from unittest import TestCase

from notion_api.common.domain.tag_relation import TagRelation


class TestTagRelation(TestCase):
    def test_変換する(self):
        # Given
        input = ["12345", "12345", "abcde"]

        # When
        actual = TagRelation.empty().from_id_list(input)

        # Then
        self.assertEqual(2, len(actual.id_list))
