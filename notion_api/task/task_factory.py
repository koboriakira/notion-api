from datetime import date, datetime

from notion_client_wrapper.block.block import Block
from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.title import Title
from task.domain.due_date import DueDate
from task.domain.task import Task
from task.domain.task_kind import TaskKind, TaskKindType
from task.domain.task_start_date import TaskStartDate
from task.domain.task_status import TaskStatus, TaskStatusType


class TaskFactory:
    @classmethod
    def create_todo_task(  # noqa: PLR0913
        cls: "TaskFactory",
        title: str | Title,
        task_kind_type: TaskKindType | None = None,
        start_date: datetime | date | None = None,
        due_date: datetime | date | None = None,
        status: TaskStatusType | None = None,
        blocks: list[Block] | None = None,
    ) -> Task:
        blocks = blocks or []
        properties = [
            title if isinstance(title, Title) else Title.from_plain_text(text=title),
        ]
        if task_kind_type is not None:
            properties.append(TaskKind.create(task_kind_type))
        if start_date is not None:
            properties.append(TaskStartDate.create(start_date))
        if due_date is not None:
            properties.append(DueDate.create(due_date))
        if status is not None:
            properties.append(TaskStatus.from_status_type(status))
        return Task(properties=Properties(values=properties), block_children=blocks)
