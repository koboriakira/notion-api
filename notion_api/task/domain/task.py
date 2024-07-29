import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import override

from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.page.page_id import PageId
from task.domain.do_tomorrow_flag import DoTommorowFlag
from task.domain.due_date import DueDate
from task.domain.pomodoro_counter import PomodoroCounter
from task.domain.pomodoro_start_datetime import PomodoroStartDatetime
from task.domain.project_relation import ProjectRelation
from task.domain.task_context import TaskContext, TaskContextType
from task.domain.task_kind import TaskKind, TaskKindType
from task.domain.task_start_date import TaskStartDate
from task.domain.task_status import TaskStatus, TaskStatusType
from util.datetime import convert_to_date_or_datetime, jst_now

COLUMN_NAME_TITLE = "名前"
COLUMN_NAME_STATUS = "ステータス"
COLUMN_NAME_START_DATE = "実施日"
COLUMN_NAME_KIND = "タスク種別"


@dataclass
class ToDoTask(BasePage):
    def update_status(self, status: str | TaskStatusType) -> "ToDoTask":
        if isinstance(status, str):
            status = TaskStatusType.from_text(status)
        task_status = TaskStatus.from_status_type(status)
        properties = self.properties.append_property(task_status)
        self.properties = properties
        return self

    def update_start_datetime(self, start_datetime: datetime | date | None) -> "ToDoTask":
        start_date = TaskStartDate.create(start_datetime)
        properties = self.properties.append_property(start_date)
        self.properties = properties
        return self

    def update_pomodoro_count(self, number: int) -> "ToDoTask":
        pomodoro_counter = PomodoroCounter(number=number)
        pomodoro_start_datetime = PomodoroStartDatetime(jst_now())
        self.properties = self.properties.append_property(pomodoro_counter).append_property(pomodoro_start_datetime)
        return self

    def do_tomorrow(self) -> "ToDoTask":
        do_tomorrow_flag = DoTommorowFlag.false()
        self.properties = self.properties.append_property(do_tomorrow_flag)
        if self.start_date is not None:
            start_date = TaskStartDate.create(self.start_date + timedelta(days=1))
            self.properties = self.properties.append_property(start_date)
        if self.due_date is not None:
            due_date = DueDate.create(self.due_date + timedelta(days=1))
            self.properties = self.properties.append_property(due_date)
        return self

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
    def start_date(self) -> date | datetime | None:
        start_date_model = self.get_date(name=TaskStartDate.NAME)
        if start_date_model is None or start_date_model.start is None:
            return None
        return convert_to_date_or_datetime(value=start_date_model.start)

    @property
    def due_date(self) -> date | datetime | None:
        due_date_model = self.get_date(name=DueDate.NAME)
        if due_date_model is None or due_date_model.start is None:
            return None
        return convert_to_date_or_datetime(value=due_date_model.start)

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

    @property
    def is_do_tomorrow(self) -> bool:
        return self.get_checkbox(name=DoTommorowFlag.NAME).checked

    @property
    def is_important(self) -> bool:
        return False

    @property
    def context(self) -> list[TaskContextType]:
        context = self.get_multi_select(name=TaskContext.NAME)
        if context is None:
            return []
        return [TaskContextType.from_text(el.name) for el in context.values]

    @property
    def order(self) -> int:
        """
        場合は該当時刻のタイムスタンプを、
        それ以外はすべて優先度最低(sys.maxsize)にする
        """
        now = jst_now().timestamp()
        if (
            isinstance(self.due_date, datetime)
            and self.due_date.time() != datetime.min.time()
            and (self.due_date - timedelta(minutes=60)).timestamp() <= now
        ):
            return int(self.due_date.timestamp())
        if self.kind is not None:
            # kindの優先度が高いほどorderを小さくする
            return sys.maxsize - self.kind.priority
        return sys.maxsize

    @property
    def pomodoro_start_datetime(self) -> datetime | None:
        pomodoro_start_datetime = self.get_date(name=PomodoroStartDatetime.NAME)
        if pomodoro_start_datetime is None or pomodoro_start_datetime.start is None:
            return None
        return convert_to_date_or_datetime(value=pomodoro_start_datetime.start, cls=datetime)

    def is_kind_trash(self) -> bool:
        return self.kind == TaskKindType.TRASH

    def has_start_datetime(self) -> bool:
        return self.start_datetime is not None


class ImportantToDoTask(ToDoTask):
    @property
    @override
    def order(self) -> int:
        return 1

    @property
    @override
    def is_important(self) -> bool:
        return True


class ScheduledTask(ToDoTask):
    @property
    @override
    def order(self) -> int:
        """
        開始時間の30分前になる場合は該当時刻のタイムスタンプを、
        それ以外はすべて優先度最低(sys.maxsize)にする
        """
        now = jst_now().timestamp()
        if (
            isinstance(self.start_date, datetime)
            and self.start_date.time() != datetime.min.time()
            and (self.start_date - timedelta(minutes=30)).timestamp() <= now
        ):
            return int(self.start_date.timestamp() - 1)
        return sys.maxsize


type Task = ToDoTask | ImportantToDoTask | ScheduledTask
