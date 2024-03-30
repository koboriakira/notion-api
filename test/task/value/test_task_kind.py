from unittest import TestCase

from notion_api.domain.task.task_kind import TaskKind, TaskKindType


class TestTaskKind(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_create(self):
        # When
        actual = TaskKind.create(kind_type=TaskKindType.NEXT_ACTION)

        # Then
        self.assertEqual(TaskKindType.NEXT_ACTION.selected_name, actual.selected_name)
        self.assertEqual(TaskKindType.NEXT_ACTION.selected_id, actual.selected_id)
        self.assertEqual(TaskKindType.NEXT_ACTION.selected_color, actual.selected_color)
