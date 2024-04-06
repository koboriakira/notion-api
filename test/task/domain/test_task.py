from datetime import datetime
from unittest import TestCase

from notion_api.task.domain.task import Task
from notion_api.task.domain.task_kind import TaskKindType
from notion_api.task.domain.task_status import TaskStatusType


class TestTask(TestCase):
    def test_タスクを作成する(self):
        # Given
        title = "title"
        task_kind_type = TaskKindType.NEXT_ACTION
        start_date = datetime(2024, 3, 20)
        status = TaskStatusType.TODO

        # When
        actual = Task.create(
            title=title,
            task_kind_type=task_kind_type,
            start_date=start_date,
            status=status
        )

        # Then
        self.assertEqual(title, actual.get_title().text)
        self.assertEqual(task_kind_type.value, actual.kind.value)
        self.assertEqual(start_date, actual.start_datetime)
        self.assertEqual(status.value, actual.status.value)
