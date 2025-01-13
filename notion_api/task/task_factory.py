from datetime import date, datetime
from typing import TYPE_CHECKING

from lotion import BasePage
from lotion.block import Block
from lotion.block.rich_text import RichText
from lotion.properties import Properties, Title

from notion_databases.task import ProjectRelation, Task, TaskContext, TaskKind, TaskStartDate, TaskStatus
from notion_databases.task_prop.task_context import TaskContextTypes
from notion_databases.task_prop.task_kind import TaskKindType
from notion_databases.task_prop.task_status import TaskStatusType

if TYPE_CHECKING:
    from lotion.properties import Property


class TaskFactory:
    @classmethod
    def create_todo_task(  # noqa: C901, PLR0913
        cls,
        title: str | RichText,
        task_kind_type: TaskKindType | None = None,
        start_date: datetime | date | None = None,
        end_date: datetime | date | None = None,
        context_types: TaskContextTypes | None = None,
        project_id: str | None = None,
        status: TaskStatusType | None = None,
        blocks: list[Block] | None = None,
    ) -> Task:
        blocks = blocks or []
        properties: list[Property] = []
        properties.append(Title.from_plain_text(title) if isinstance(title, str) else Title.from_rich_text(title))
        if task_kind_type is not None:
            properties.append(TaskKind.from_name(task_kind_type.value))
        if start_date is not None:
            if end_date is None:
                properties.append(TaskStartDate.from_start_date(start_date))
            else:
                properties.append(TaskStartDate.from_range(start_date, end_date))
        if context_types is not None:
            properties.append(TaskContext.from_name(context_types.to_str_list()))
        if status is not None:
            properties.append(TaskStatus.from_status_type(status))
        if project_id is not None:
            properties.append(ProjectRelation.from_id(project_id))
        return Task(properties=Properties(values=properties), block_children=blocks)

    @staticmethod
    def cast(base_page: BasePage) -> Task:
        return Task(
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
