from dataclasses import dataclass
from datetime import date, datetime

from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.page.page_id import PageId
from task.domain.pomodoro_counter import PomodoroCounter
from task.domain.project_relation import ProjectRelation
from task.domain.task_kind import TaskKind, TaskKindType
from task.domain.task_start_date import TaskStartDate
from task.domain.task_status import TaskStatus, TaskStatusType
from util.datetime import convert_to_date_or_datetime

COLUMN_NAME_TITLE = "名前"
COLUMN_NAME_STATUS = "ステータス"
COLUMN_NAME_START_DATE = "実施日"
COLUMN_NAME_KIND = "タスク種別"


@dataclass
class Task(BasePage):
    def update_status(self, status: str | TaskStatusType) -> None:
        if isinstance(status, str):
            status = TaskStatusType.from_text(status)
        task_status = TaskStatus.from_status_type(status)
        properties = self.properties.append_property(task_status)
        self.properties = properties

    def update_start_datetime(self, start_datetime: datetime | date | None) -> None:
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
    def start_datetime(self) -> datetime | None:
        start_date_model = self.get_date(name=TaskStartDate.NAME)
        if start_date_model is None or start_date_model.start is None:
            return None
        return convert_to_date_or_datetime(value=start_date_model.start, cls=datetime)

    @property
    def start_date(self) -> date | None:
        start_date_model = self.get_date(name=TaskStartDate.NAME)
        if start_date_model is None or start_date_model.start is None:
            return None
        return convert_to_date_or_datetime(value=start_date_model.start, cls=date)

    @property
    def kind(self) -> TaskKindType | None:
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

    @property
    def project_id_list(self) -> list[PageId]:
        project_relation = self.get_relation(name=ProjectRelation.NAME)
        if project_relation is None:
            return []
        return project_relation.page_id_list

    def is_kind_trash(self) -> bool:
        return self.kind == TaskKindType.TRASH

    def has_start_datetime(self) -> bool:
        return self.start_datetime is not None
