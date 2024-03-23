from dataclasses import dataclass
from datetime import date, datetime

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


    @property
    def status(self) -> TaskStatusType:
        status_name = self.get_status(name=COLUMN_NAME_STATUS).status_name
        return TaskStatusType(status_name)

    @property
    def start_datetime(self) -> datetime|date|None:
        start_date_model = self.get_date(name=COLUMN_NAME_START_DATE)
        if start_date_model is None or start_date_model.start is None:
            return None
        return _convert_to_datetime(start_date_model.start)

    @property
    def kind(self) -> TaskKindType|None:
        kind_model = self.get_select(name=COLUMN_NAME_KIND)
        if kind_model is None or kind_model.selected_name is None:
            return None
        return TaskKindType(kind_model.selected_name)

    def is_kind_trash(self) -> bool:
        return self.kind == TaskKindType.TRASH

    def has_start_datetime(self) -> bool:
        return self.start_datetime is not None

def _convert_to_datetime(value: str) -> datetime|date:
    return convert_to_date_or_datetime(value)
