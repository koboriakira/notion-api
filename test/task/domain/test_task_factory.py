from datetime import date
from unittest import TestCase

from notion_api.task.domain.task_kind import TaskKindType
from notion_api.task.domain.task_status import TaskStatusType

from task.task_factory import TaskFactory


class TestTaskFactory(TestCase):
    def test_TODOタスクを作成する(self):
        # Given
        title = "title"
        task_kind_type = TaskKindType.NEXT_ACTION
        start_date = date(2024, 3, 20)
        status = TaskStatusType.TODO

        # When
        actual = TaskFactory.create_todo_task(
            title=title, task_kind_type=task_kind_type, start_date=start_date, status=status
        )

        # Then
        self.assertEqual(title, actual.get_title().text)
        self.assertEqual(task_kind_type.value, actual.kind.to_enum().value)
        self.assertEqual(start_date, actual.start_date)
        self.assertEqual(status.value, actual.status.to_enum().value)
