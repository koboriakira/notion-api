from dataclasses import dataclass
from datetime import date, datetime

from domain.task.pomodoro_counter import PomodoroCounter
from domain.task.task_kind import TaskKind, TaskKindType
from domain.task.task_start_date import TaskStartDate
from domain.task.task_status import TaskStatus, TaskStatusType
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.block.block import Block
from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.title import Title
from util.datetime import convert_to_date_or_datetime

COLUMN_NAME_TITLE = "名前"
COLUMN_NAME_STATUS = "ステータス"
COLUMN_NAME_START_DATE = "実施日"
COLUMN_NAME_KIND = "タスク種別"

@dataclass
class Task(BasePage):
    @staticmethod
    def create(
            title: str|Title,
            task_kind_type: TaskKindType|None = None,
            start_date: datetime|date|None = None,
            status: TaskStatusType|None = None,
            blocks: list[Block]|None = None) -> "Task":
        blocks = blocks or []
        properties = [
            title if isinstance(title, Title) else Title.from_plain_text(name=COLUMN_NAME_TITLE, text=title),
        ]
        if task_kind_type is not None:
            properties.append(TaskKind.create(task_kind_type))
        if start_date is not None:
            properties.append(TaskStartDate.create(start_date))
        if status is not None:
            properties.append(TaskStatus.from_status_type(status))
        return Task(properties=Properties(values=properties), block_children=blocks)

    def update_status(self, status: str|TaskStatusType) -> None:
        if isinstance(status, str):
            status = TaskStatusType.from_text(status)
        task_status = TaskStatus.from_status_type(status)
        properties = self.properties.append_property(task_status)
        self.properties = properties

    def update_start_datetime(self, start_datetime: datetime|date|None) -> None:
        start_date = TaskStartDate.create(start_datetime)
        properties = self.properties.append_property(start_date)
        self.properties = properties

    def update_pomodoro_count(self, number: int) -> None:
        pomodoro_counter = PomodoroCounter(number=number)
        properties = self.properties.append_property(pomodoro_counter)
        self.properties = properties

    @property
    def status(self) -> TaskStatusType:
        status_name = self.get_status(name=TaskStatus.NAME).status_name
        return TaskStatusType(status_name)

    @property
    def start_datetime(self) -> datetime|None:
        start_date_model = self.get_date(name=TaskStartDate.NAME)
        if start_date_model is None or start_date_model.start is None:
            return None
        return convert_to_date_or_datetime(value=start_date_model.start, cls=datetime)

    @property
    def start_date(self) -> date|None:
        start_date_model = self.get_date(name=TaskStartDate.NAME)
        if start_date_model is None or start_date_model.start is None:
            return None
        return convert_to_date_or_datetime(value=start_date_model.start, cls=date)

    @property
    def kind(self) -> TaskKindType|None:
        kind_model = self.get_select(name=TaskKind.NAME)
        if kind_model is None or kind_model.selected_name is None:
            return None
        return TaskKindType(kind_model.selected_name)

    @property
    def pomodoro_count(self) -> int:
        pomodoro_counter = self.get_number(name=PomodoroCounter.NAME)
        if pomodoro_counter is None:
            return 0
        return pomodoro_counter.number or 0

    def is_kind_trash(self) -> bool:
        return self.kind == TaskKindType.TRASH

    def has_start_datetime(self) -> bool:
        return self.start_datetime is not None
