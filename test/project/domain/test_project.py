from datetime import date
from unittest import TestCase

from notion_api.project.domain.importance import ImportanceType
from notion_api.project.domain.project import Project
from notion_api.project.domain.project_status import ProjectStatusType
from notion_api.project.domain.schedule import Schedule


class TestProject(TestCase):
    def test_インスタンスの生成(self):
        # When
        actual = Project.create(
            title="iDeCoの移管をする",
            project_status=ProjectStatusType.IN_PROGRESS,
            importance=ImportanceType.THREE,
            definition_of_done="iDeCoの移管が完了している",
            weekly_goal="iDeCoの移管をする",
            goal_relation=["abc123", "def456"],
            schedule=Schedule.create(
                start_date=date.fromisoformat("2024-02-13"),
                end_date=date.fromisoformat("2024-03-30"),
            ),
            tag_relation=["abc123", "def456"],
        )

        # Then
        self.assertEqual(actual.project_name, "iDeCoの移管をする")
        self.assertEqual(actual.project_status.value, "In progress")
        self.assertEqual(actual.importance.value, "⭐⭐⭐")
        self.assertEqual(actual.definition_of_done, "iDeCoの移管が完了している")
        self.assertEqual(actual.weekly_goal, "iDeCoの移管をする")
        actual_goal_list = actual.goal_relation
        self.assertCountEqual(actual_goal_list, ["abc123", "def456"])
        self.assertTrue("abc123" in actual_goal_list)
        self.assertTrue("def456" in actual_goal_list)
        self.assertEqual(actual.schedule.start_date, date.fromisoformat("2024-02-13"))
        self.assertEqual(actual.schedule.end_date, date.fromisoformat("2024-03-30"))
        actual_tag_list = actual.tag_relation
        self.assertCountEqual(actual_tag_list, ["abc123", "def456"])
        self.assertTrue("abc123" in actual_tag_list)
        self.assertTrue("def456" in actual_tag_list)
        self.assertEqual(actual.cover, None)
        self.assertEqual(actual.block_children, [])
