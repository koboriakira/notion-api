from datetime import date, datetime
from typing import TYPE_CHECKING

from lotion import BasePage
from lotion.block import Block
from lotion.properties import Properties, Title

from task.domain.project_relation import ProjectRelation
from task.domain.task import ToDoTask
from task.domain.task_context import TaskContext, TaskContextTypes
from task.domain.task_kind import TaskKind, TaskKindType
from task.domain.task_start_date import TaskStartDate
from task.domain.task_status import TaskStatus, TaskStatusType

if TYPE_CHECKING:
    from lotion.properties import Property


class TaskFactory:
    @classmethod
    def create_todo_task(  # noqa: C901, PLR0913
        cls,
        title: str | Title,
        task_kind_type: TaskKindType | None = None,
        start_date: datetime | date | None = None,
        end_date: datetime | date | None = None,
        context_types: TaskContextTypes | None = None,
        project_id: str | None = None,
        status: TaskStatusType | None = None,
        blocks: list[Block] | None = None,
    ) -> ToDoTask:
        blocks = blocks or []
        properties: list[Property] = []
        properties.append(title if isinstance(title, Title) else Title.from_plain_text(text=title))
        if task_kind_type is not None:
            properties.append(TaskKind.create(task_kind_type))
        if start_date is not None:
            properties.append(TaskStartDate.create(start_date, end_date))
        if context_types is not None:
            properties.append(TaskContext(context_types))
        if status is not None:
            properties.append(TaskStatus.from_status_type(status))
        if project_id is not None:
            properties.append(ProjectRelation.from_id(project_id))
        return ToDoTask(properties=Properties(values=properties), block_children=blocks)

    @staticmethod
    def cast(base_page: BasePage) -> ToDoTask:
        return ToDoTask(
            properties=base_page.properties,
            block_children=base_page.block_children,
            id_=base_page.id_,
            url_=base_page.url_,
            created_time=base_page.created_time,
            last_edited_time=base_page.last_edited_time,
            _created_by=base_page._created_by,  # noqa: SLF001
            _last_edited_by=base_page._last_edited_by,  # noqa: SLF001
            cover=base_page.cover,
            icon=base_page.icon,
            archived=base_page.archived,
            parent=base_page.parent,
        )
