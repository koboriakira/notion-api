from datetime import date
from unittest import TestCase

from notion_databases.goal import Goal, GoalStatusType

DUMMY_PAGE_ID = "5c38fd30-714b-4ce2-bf2d-25407f3cfc16"


class TestGoal(TestCase):
    def test_インスタンスの生成(self):
        # When
        actual = Goal.generate(
            title="日々の管理システムを構築する",
            goal_status=GoalStatusType.IN_PROGRESS,
            project_relation=[DUMMY_PAGE_ID],
            vision_relation=[DUMMY_PAGE_ID],
            due_date=date.fromisoformat("2024-03-31"),
        )

        # Then
        self.assertEqual(actual.title.text, "日々の管理システムを構築する")
        self.assertEqual(actual.status.status_name, "In progress")
        actual_project_list = actual.project_relation.id_list
        self.assertCountEqual(actual_project_list, [DUMMY_PAGE_ID])
        self.assertTrue(DUMMY_PAGE_ID in actual_project_list)
        actual_vision_list = actual.vision_relation.id_list
        self.assertCountEqual(actual_vision_list, [DUMMY_PAGE_ID])
        self.assertTrue(DUMMY_PAGE_ID in actual_vision_list)
        self.assertEqual(actual.due_date.date, date.fromisoformat("2024-03-31"))
