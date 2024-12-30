from datetime import date
from unittest import TestCase

from notion_api.project.domain.importance import ImportanceType
from notion_api.project.domain.project import Importance, Project
from notion_api.project.domain.project_status import ProjectStatusType


class TestProject(TestCase):
    def test_インスタンスの生成(self):
        # Given
        importance_type = ImportanceType.THREE
        importance = Importance.from_name(importance_type.value)

        # When
        actual = Project.generate(
            title="iDeCoの移管をする",
            project_status=ProjectStatusType.IN_PROGRESS,
            importance=importance,
            definition_of_done="iDeCoの移管が完了している",
            weekly_goal="iDeCoの移管をする",
            goal_relation=["abc123", "def456"],
            start=date.fromisoformat("2024-02-13"),
            end=date.fromisoformat("2024-03-30"),
            tag_relation=["abc123", "def456"],
        )

        # Then
        self.assertEqual(actual.title.text, "iDeCoの移管をする")
        self.assertEqual(actual.status.status_name, "In progress")
        self.assertEqual(actual.importance.selected_name, importance_type.value)
        self.assertEqual(actual.definition_of_done.text, "iDeCoの移管が完了している")
        self.assertEqual(actual.weekly_goal.text, "iDeCoの移管をする")
        actual_goal_list = actual.goal.id_list
        self.assertCountEqual(actual_goal_list, ["abc123", "def456"])
        self.assertTrue("abc123" in actual_goal_list)
        self.assertTrue("def456" in actual_goal_list)
        self.assertEqual(actual.schedule.start_date, date.fromisoformat("2024-02-13"))
        self.assertEqual(actual.schedule.end_date, date.fromisoformat("2024-03-30"))
        actual_tag_list = actual.tags.id_list
        self.assertCountEqual(actual_tag_list, ["abc123", "def456"])
        self.assertTrue("abc123" in actual_tag_list)
        self.assertTrue("def456" in actual_tag_list)
        self.assertEqual(actual.cover, None)
        self.assertEqual(actual.block_children, [])
