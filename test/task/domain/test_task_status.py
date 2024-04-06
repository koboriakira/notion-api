from unittest import TestCase

from notion_api.task.domain.task_status import TaskStatusType


class TestTaskStatusType(TestCase):
    def test_変換する(self):
        # Given
        input = ["ToDO", "InProgress"]

        # When
        actual = TaskStatusType.get_status_list(input)

        # Then
        self.assertEqual(2, len(actual))
        self.assertEqual("ToDo", actual[0].value)
        self.assertEqual("InProgress", actual[1].value)
