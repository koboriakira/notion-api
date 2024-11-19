from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import override

from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.page.page_id import PageId
from task.domain.completed_flag import CompletedFlag
from task.domain.do_tomorrow_flag import DoTommorowFlag
from task.domain.due_date import DueDate
from task.domain.is_started import IsStarted
from task.domain.later_flag import LaterFlag
from task.domain.pomodoro_counter import PomodoroCounter
from task.domain.pomodoro_start_datetime import PomodoroStartDatetime
from task.domain.project_relation import ProjectRelation
from task.domain.task_context import TaskContext, TaskContextType
from task.domain.task_kind import TaskKind, TaskKindType
from task.domain.task_start_date import TaskStartDate
from task.domain.task_status import TaskStatus, TaskStatusType
from task.valueobject.task_order import TaskOrder
from task.valueobject.task_order_rule import TaskOrderRule
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

    def update_kind(self, kind: TaskKindType) -> "ToDoTask":
        self.properties = self.properties.append_property(TaskKind.create(kind))
        return self

    def update_start_datetime(
        self,
        start_datetime: datetime | date | None,
        end_datetime: datetime | date | None,
    ) -> "ToDoTask":
        start_date = TaskStartDate.create(start_datetime, end_datetime)
        properties = self.properties.append_property(start_date)
        self.properties = properties
        return self

    def update_pomodoro_count(self, number: int) -> "ToDoTask":
        pomodoro_counter = PomodoroCounter(number=number)
        pomodoro_start_datetime = PomodoroStartDatetime(jst_now())
        self.properties = self.properties.append_property(pomodoro_counter).append_property(pomodoro_start_datetime)
        return self

    def reset_is_started(self) -> "ToDoTask":
        self.properties = self.properties.append_property(IsStarted.false())
        return self

    def reset_is_completed(self) -> "ToDoTask":
        self.properties = self.properties.append_property(CompletedFlag.false())
        return self

    def reset_later_flag(self) -> "ToDoTask":
        self.properties = self.properties.append_property(LaterFlag.false())
        return self

    def do_tomorrow(self) -> "ToDoTask":
        do_tomorrow_flag = DoTommorowFlag.false()
        self.properties = self.properties.append_property(do_tomorrow_flag)
        if self.start_date is not None:
            date_ = self.start_date.date() if isinstance(self.start_date, datetime) else self.start_date
            start_date = TaskStartDate.create(date_ + timedelta(days=1))
            self.properties = self.properties.append_property(start_date)
        if self.due_date is not None:
            due_date = DueDate.create(self.due_date + timedelta(days=1))
            self.properties = self.properties.append_property(due_date)
        return self

    def start(self) -> "ToDoTask":
        start = jst_now()
        end = start + timedelta(minutes=30)
        return (
            self.update_status(TaskStatusType.IN_PROGRESS)
            .update_pomodoro_count(number=self.pomodoro_count + 1)
            .reset_is_started()
            .update_start_datetime(start, end)
        )

    def complete(self) -> "ToDoTask":
        return self.update_status(TaskStatusType.DONE).reset_is_completed().update_start_end_datetime(end=jst_now())


    def update_start_end_datetime(self, end: datetime) -> "ToDoTask":
        """タスクの終了日時を更新する"""
        start = self.start_datetime
        if start is None:
            # 開始時刻がない場合はなにもしない
            return self
        start_date = TaskStartDate.create(start_date=start, end_date=end)
        self.properties = self.properties.append_property(start_date)
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
    def is_started(self) -> bool:
        return self.get_checkbox(name=IsStarted.NAME).checked

    @property
    def context(self) -> list[TaskContextType]:
        context = self.get_multi_select(name=TaskContext.NAME)
        if context is None:
            return []
        return [TaskContextType.from_text(el.name) for el in context.values]

    @property
    def order(self) -> int:
        return TaskOrderRule.calculate(
            start_datetime=self.start_datetime,
            due_datetime=self.due_date,
            kind=self.kind,
        ).value

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

    @property
    def is_completed_flag(self) -> bool:
        return self.get_checkbox(name=CompletedFlag.NAME).checked

    @property
    def is_started_flag(self) -> bool:
        return self.get_checkbox(name=IsStarted.NAME).checked

    @property
    def is_later_flag(self) -> bool:
        return self.get_checkbox(name=LaterFlag.NAME).checked



class ImportantToDoTask(ToDoTask):
    @property
    @override
    def order(self) -> int:
        return TaskOrder.most_important().value

    @property
    @override
    def is_important(self) -> bool:
        return True


class ScheduledTask(ToDoTask):
    """スケジュールされたタスク"""


class RoutineToDoTask(ToDoTask):
    """ルーティン系のタスク"""


type Task = ToDoTask | ImportantToDoTask | ScheduledTask | RoutineToDoTask
