from dataclasses import dataclass
from datetime import date

from goal.domain.due_date import DueDate
from goal.domain.goal_name import GoalName
from goal.domain.goal_status import GoalStatus, GoalStatusType
from goal.domain.project_relation import ProjectRelation
from goal.domain.vision_relation import VisionRelation
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.block.block import Block
from notion_client_wrapper.page.page_id import PageId
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.properties import Properties


@dataclass
class Goal(BasePage):
    @staticmethod
    def create(  # noqa: PLR0913
        title: str | GoalName,
        goal_status: GoalStatusType | GoalStatus,
        project_relation: list[PageId] | ProjectRelation | None = None,
        vision_relation: list[PageId] | VisionRelation | None = None,
        due_date: DueDate | date | None = None,
        blocks: list[Block] | None = None,
        cover: str | Cover | None = None,
    ) -> "Goal":
        blocks = blocks or []
        properties = [
            title if isinstance(title, GoalName) else GoalName(text=title),
            (
                goal_status
                if isinstance(goal_status, GoalStatus)
                else GoalStatus.from_status_type(status_type=goal_status)
            ),
        ]
        if project_relation is not None:
            project_relation = (
                project_relation
                if isinstance(project_relation, ProjectRelation)
                else ProjectRelation.from_id_list(id_list=project_relation)
            )
            properties.append(project_relation)
        if vision_relation is not None:
            vision_relation = (
                vision_relation
                if isinstance(vision_relation, VisionRelation)
                else VisionRelation.from_id_list(id_list=vision_relation)
            )
            properties.append(vision_relation)
        if due_date is not None:
            due_date = due_date if isinstance(due_date, DueDate) else DueDate.create(due_date)
            properties.append(due_date)
        if cover is None:
            return Goal(properties=Properties(values=properties), block_children=blocks)
        cover = cover if isinstance(cover, Cover) else Cover.from_external_url(cover)
        return Goal(properties=Properties(values=properties), block_children=blocks, cover=cover)

    @property
    def goal_name(self) -> str:
        return self.get_title_text()

    @property
    def project_relation(self) -> list[str]:
        return self.get_relation(name=ProjectRelation.NAME).id_list

    @property
    def vision_relation(self) -> list[str]:
        return self.get_relation(name=VisionRelation.NAME).id_list

    @property
    def due_date(self) -> date | None:
        due_date = self.get_date(name=DueDate.NAME)
        return due_date.start_date if due_date is not None else None

    @property
    def goal_status(self) -> GoalStatusType:
        return GoalStatusType.from_text(text=self.get_status(name=GoalStatus.NAME).status_name)
