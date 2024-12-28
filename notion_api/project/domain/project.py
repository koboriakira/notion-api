from datetime import date, datetime

from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.block import Block
from lotion.properties import Cover, Date, Property, Relation, Select, Text, Title

from common.domain.tag_relation import TagRelation
from common.value.database_type import DatabaseType
from project.domain.project_status import ProjectStatus, ProjectStatusType


@notion_prop("名前")
class ProjectName(Title):
    pass


@notion_prop("ゴール")
class DefinitionOfDone(Text):
    pass


@notion_prop("目標")
class GoalRelation(Relation):
    pass


@notion_prop("重要度")
class Importance(Select):
    pass


@notion_prop("開始可能日")
class Schedule(Date):
    pass


@notion_prop("今週の目標")
class WeeklyGoal(Text):
    pass


@notion_database(DatabaseType.PROJECT.value)
class Project(BasePage):
    title: ProjectName
    definition_of_done: DefinitionOfDone
    status: ProjectStatus
    tags: TagRelation
    weekly_goal: WeeklyGoal
    goal: GoalRelation
    schedule: Schedule
    importance: Importance
    # task_relation:

    def is_done(self) -> bool:
        return self._get_status_type().is_done()

    def is_trash(self) -> bool:
        return self._get_status_type().is_trash()

    def is_inprogress(self) -> bool:
        return self._get_status_type().is_in_progress()

    def is_inbox(self) -> bool:
        return self._get_status_type().is_inbox()

    def _get_status_type(self) -> ProjectStatusType:
        return ProjectStatusType.from_text(text=self.status.status_name)

    @staticmethod
    def generate(  # noqa: C901, PLR0913
        title: str,
        project_status: ProjectStatusType | None,
        importance: Importance | None = None,
        definition_of_done: str | None = None,
        weekly_goal: str | None = None,
        goal_relation: list[str] | None = None,
        start: date | datetime | None = None,
        end: date | datetime | None = None,
        tag_relation: list[str] | None = None,
        blocks: list[Block] | None = None,
        cover: str | None = None,
    ) -> "Project":
        blocks = blocks or []
        properties: list[Property] = []
        properties.append(ProjectName.from_plain_text(title))
        if project_status is not None:
            properties.append(ProjectStatus.from_status_type(project_status))
        if importance is not None:
            properties.append(importance)
        if definition_of_done is not None:
            properties.append(DefinitionOfDone.from_plain_text(definition_of_done))
        if weekly_goal is not None:
            properties.append(WeeklyGoal.from_plain_text(weekly_goal))
        if goal_relation is not None:
            properties.append(GoalRelation.from_id_list(goal_relation))
        if tag_relation is not None:
            properties.append(TagRelation.from_id_list(tag_relation))
        if start is not None:
            if end is None:
                properties.append(Schedule.from_start_date(start))
            else:
                properties.append(Schedule.from_range(start, end))
        if cover is None:
            return Project.create(properties, blocks)
        return Project.create(properties, blocks, cover=Cover.from_external_url(cover))
