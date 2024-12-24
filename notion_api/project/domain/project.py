from dataclasses import dataclass

from lotion.base_page import BasePage
from lotion.block import Block
from lotion.properties import Cover, Properties

from common.domain.tag_relation import TagRelation
from project.domain.definition_of_done import DefinitionOfDone
from project.domain.goal_relation import GoalRelation
from project.domain.importance import Importance, ImportanceType
from project.domain.project_name import ProjectName
from project.domain.project_status import ProjectStatus, ProjectStatusType
from project.domain.schedule import Schedule
from project.domain.weekly_goal import WeeklyGoal


@dataclass
class Project(BasePage):
    @staticmethod
    def create(  # noqa: C901, PLR0913
        title: str | ProjectName,
        project_status: ProjectStatusType | ProjectStatus | None,
        importance: ImportanceType | Importance | None = None,
        definition_of_done: str | DefinitionOfDone | None = None,
        weekly_goal: str | WeeklyGoal | None = None,
        goal_relation: list[str] | GoalRelation | None = None,
        schedule: Schedule | None = None,
        tag_relation: list[str] | TagRelation | None = None,
        # TODO: タグもエンティティとして持ちたい
        blocks: list[Block] | None = None,
        cover: str | Cover | None = None,
    ) -> "Project":
        blocks = blocks or []
        properties = [
            title if isinstance(title, ProjectName) else ProjectName(text=title),
            (
                project_status
                if isinstance(project_status, ProjectStatus)
                else ProjectStatus.from_status_type(status_type=project_status)
            ),
        ]
        if importance is not None:
            importance = importance if isinstance(importance, Importance) else Importance.create(kind_type=importance)
            properties.append(importance)
        if definition_of_done is not None:
            definition_of_done = (
                definition_of_done
                if isinstance(definition_of_done, DefinitionOfDone)
                else DefinitionOfDone.from_plain_text(text=definition_of_done)
            )
            properties.append(definition_of_done)
        if weekly_goal is not None:
            weekly_goal = (
                weekly_goal if isinstance(weekly_goal, WeeklyGoal) else WeeklyGoal.from_plain_text(text=weekly_goal)
            )
            properties.append(weekly_goal)
        if goal_relation is not None:
            goal_relation = (
                goal_relation
                if isinstance(goal_relation, GoalRelation)
                else GoalRelation.from_id_list(id_list=goal_relation)
            )
            properties.append(goal_relation)
        if tag_relation is not None:
            tag_relation = (
                tag_relation
                if isinstance(tag_relation, TagRelation)
                else TagRelation.from_id_list(id_list=tag_relation)
            )
            properties.append(tag_relation)
        if schedule is not None:
            properties.append(schedule)
        if cover is None:
            return Project(properties=Properties(values=properties), block_children=blocks)
        cover = cover if isinstance(cover, Cover) else Cover.from_external_url(cover)
        return Project(properties=Properties(values=properties), block_children=blocks, cover=cover)

    def update_tag_relation(self, tag_relation: TagRelation) -> None:
        properties = self.properties.append_property(tag_relation)
        self.properties = properties

    @property
    def project_name(self) -> str:
        return self.get_title_text()

    @property
    def definition_of_done(self) -> str:
        return self.get_text(name=DefinitionOfDone.NAME).text

    @property
    def weekly_goal(self) -> str:
        return self.get_text(name=WeeklyGoal.NAME).text

    @property
    def goal_relation(self) -> list[str]:
        return self.get_relation(name=GoalRelation.NAME).id_list

    @property
    def schedule(self) -> Schedule | None:
        return self.get_date(name=Schedule.NAME)

    @property
    def tag_relation(self) -> list[str]:
        return self.get_relation(name=TagRelation.NAME).id_list

    @property
    def importance(self) -> ImportanceType:
        return ImportanceType.from_text(text=self.get_select(name=Importance.NAME).selected_name)

    @property
    def project_status(self) -> ProjectStatusType:
        return ProjectStatusType.from_text(text=self.get_status(name=ProjectStatus.NAME).status_name)

    @property
    def status(self) -> ProjectStatusType:
        return self.project_status
