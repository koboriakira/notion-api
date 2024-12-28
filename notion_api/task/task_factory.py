from datetime import date, datetime
from typing import TYPE_CHECKING

from lotion import BasePage
from lotion.block import Block
from lotion.properties import Properties, Text, Title

from task.domain.important_flag import ImportantFlag
from task.domain.pomodoro_start_datetime import PomodoroStartDatetime
from task.domain.project_relation import ProjectRelation
from task.domain.routine_kind import RoutineKind, RoutineType
from task.domain.routine_task import RoutineTask
from task.domain.task import ImportantToDoTask, RoutineToDoTask, ScheduledTask, Task, ToDoTask
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
        pomodoro_start_datetime: datetime | None = None,
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
        if pomodoro_start_datetime is not None:
            properties.append(PomodoroStartDatetime(pomodoro_start_datetime))
        if project_id is not None:
            properties.append(ProjectRelation.from_id(project_id))
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

    @staticmethod
    def cast(base_page: BasePage) -> Task:
        cls = ToDoTask
        important_flag = base_page.get_checkbox(ImportantFlag.NAME)
        if important_flag is not None and important_flag.checked:
            cls = ImportantToDoTask
        kind_model = base_page.get_select(name=TaskKind.NAME)
        if kind_model is not None and kind_model.selected_name != "":
            task_type = TaskKindType(kind_model.selected_name)
            if task_type == TaskKindType.SCHEDULE:
                cls = ScheduledTask
            if task_type == TaskKindType.ROUTINE:
                cls = RoutineToDoTask
        return cls(
            properties=base_page.properties,
            block_children=base_page.block_children,
            id_=base_page.id_,
            url_=base_page.url_,
            created_time=base_page.created_time,
            last_edited_time=base_page.last_edited_time,
            _created_by=base_page._created_by,
            _last_edited_by=base_page._last_edited_by,
            cover=base_page.cover,
            icon=base_page.icon,
            archived=base_page.archived,
            parent=base_page.parent,
        )
