from datetime import date, datetime
from typing import TYPE_CHECKING

from lotion.page import PageId
from lotion.properties import Properties, Text, Title

from lotion.block import Block
from task.domain.due_date import DueDate
from task.domain.pomodoro_start_datetime import PomodoroStartDatetime
from task.domain.project_relation import ProjectRelation
from task.domain.routine_kind import RoutineKind, RoutineType
from task.domain.routine_task import RoutineTask
from task.domain.task import RoutineToDoTask, ScheduledTask, ToDoTask
from task.domain.task_context import TaskContext, TaskContextTypes
from task.domain.task_kind import TaskKind, TaskKindType
from task.domain.task_start_date import TaskStartDate
from task.domain.task_status import TaskStatus, TaskStatusType

if TYPE_CHECKING:
    from lotion.properties import Property


class TaskFactory:
    @classmethod
    def create_todo_task(  # noqa: PLR0913
        cls,
        title: str | Title,
        task_kind_type: TaskKindType | None = None,
        start_date: datetime | date | None = None,
        end_date: datetime | date | None = None,
        due_date: datetime | date | None = None,
        pomodoro_start_datetime: datetime | None = None,
        context_types: TaskContextTypes | None = None,
        project_id: PageId | None = None,
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
        if due_date is not None:
            properties.append(DueDate.create(due_date))
        if context_types is not None:
            properties.append(TaskContext(context_types))
        if status is not None:
            properties.append(TaskStatus.from_status_type(status))
        if pomodoro_start_datetime is not None:
            properties.append(PomodoroStartDatetime(pomodoro_start_datetime))
        if project_id is not None:
            properties.append(ProjectRelation.from_id(project_id.value))
        return ToDoTask(properties=Properties(values=properties), block_children=blocks)

    @classmethod
    def create_scheduled_task(
        cls,
        title: str,
        start_date: datetime | date,
        end_date: datetime | date,
    ) -> ScheduledTask:
        blocks = []
        properties: list[Property] = [
            Title.from_plain_text(text=title),
            TaskKind.scheduled(),
            TaskStartDate.create(start_date, end_date),
        ]
        return ScheduledTask(
            properties=Properties(values=properties),
            block_children=blocks,
        )

    @classmethod
    def create_routine_todo_task(
        cls,
        title: str,
        start_date: datetime,
        end_date: datetime | None = None,
        context_types: TaskContextTypes | None = None,
        blocks: list[Block] | None = None,
    ) -> RoutineToDoTask:
        blocks = blocks or []
        properties: list[Property] = [
            Title.from_plain_text(text=title),
            TaskKind.routine(),
            TaskStartDate.create(start_date, end_date),
        ]
        if context_types is not None:
            properties.append(TaskContext(context_types))
        return RoutineToDoTask(properties=Properties(values=properties), block_children=blocks)

    @classmethod
    def create_routine_task(
        cls,
        title: str,
        routine_type: RoutineType,
        due_time: str | None = None,
    ) -> RoutineTask:
        title_property = Title.from_plain_text(text=title)
        routine_kind = RoutineKind.create(routine_type)
        properties = [title_property, routine_kind]
        if due_time is not None:
            properties.append(Text.from_plain_text(name="締め切り", text=due_time))
        return RoutineTask(properties=Properties(values=properties), block_children=[])
