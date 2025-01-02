from datetime import date
from enum import Enum

from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.block import Block
from lotion.properties import Cover, Date, Relation, Status

from common.value.database_type import DatabaseType
from notion_databases.goal_prop.goal_name import GoalName
from notion_databases.goal_prop.vision_relation import VisionRelation


class GoalStatusType(Enum):
    INBOX = "Inbox"
    IN_PROGRESS = "In progress"
    SUSPEND = "Suspend"
    TRASH = "Trash"
    DONE = "Done"

    def is_inbox(self) -> bool:
        return self == GoalStatusType.INBOX

    def is_done(self) -> bool:
        return self == GoalStatusType.DONE

    def is_in_progress(self) -> bool:
        return self == GoalStatusType.IN_PROGRESS


@notion_prop("期限")
class DueDate(Date):
    pass


@notion_prop("ステータス")
class GoalStatus(Status):
    @staticmethod
    def from_status_type(status_type: GoalStatusType) -> "GoalStatus":
        return GoalStatus.from_status_name(status_type.value)


@notion_prop("プロジェクト")
class ProjectRelation(Relation):
    pass


@notion_database(DatabaseType.GOAL.value)
class Goal(BasePage):
    title: GoalName
    status: GoalStatus
    project_relation: ProjectRelation
    vision_relation: VisionRelation
    due_date: DueDate

    def is_done(self) -> bool:
        return self._get_goal_status().is_done()

    def is_in_progress(self) -> bool:
        return self._get_goal_status().is_in_progress()

    def is_inbox(self) -> bool:
        return self._get_goal_status().is_inbox()

    def _get_goal_status(self) -> GoalStatusType:
        return GoalStatusType(self.status.status_name)

    @staticmethod
    def generate(  # noqa: PLR0913
        title: str,
        goal_status: GoalStatusType = GoalStatusType.INBOX,
        project_relation: list[str] | None = None,
        vision_relation: list[str] | None = None,
        due_date: date | None = None,
        blocks: list[Block] | None = None,
        cover: str | None = None,
    ) -> "Goal":
        blocks = blocks or []
        properties = [GoalName.from_plain_text(title), GoalStatus.from_status_type(status_type=goal_status)]
        if project_relation is not None:
            properties.append(ProjectRelation.from_id_list(project_relation))
        if vision_relation is not None:
            properties.append(VisionRelation.from_id_list(vision_relation))
        if due_date is not None:
            properties.append(DueDate.from_start_date(due_date))
        if cover is None:
            return Goal.create(properties, blocks)
        return Goal.create(
            properties,
            blocks,
            cover=Cover.from_external_url(cover),
        )
