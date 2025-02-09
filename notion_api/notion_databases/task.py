from datetime import date, datetime, timedelta

from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.block.rich_text import RichTextBuilder
from lotion.properties import Checkbox, Relation, Select, Status

from common.value.database_type import DatabaseType
from notion_databases.goal import ProjectRelation
from notion_databases.task_backup import TaskBackup, TaskName, TaskStartDate
from notion_databases.task_prop.memo_genre import MemoGenreType
from notion_databases.task_prop.task_kind import TaskKindType
from notion_databases.task_prop.task_status import TaskStatusType
from task.task_order_rule import TaskOrderRule
from util.datetime import jst_now


@notion_prop("重要")
class ImportantFlag(Checkbox):
    pass


@notion_prop("ステータス")
class TaskStatus(Status):
    @staticmethod
    def from_status_type(status_type: TaskStatusType) -> "TaskStatus":
        return TaskStatus.from_status_name(status_type.value)

    def to_enum(self) -> TaskStatusType:
        return TaskStatusType(self.status_name)

    def is_done(self) -> bool:
        return self.to_enum().is_done()

    def is_in_progress(self) -> bool:
        return self.to_enum().is_in_progress()

    def is_todo(self) -> bool:
        return self.to_enum().is_todo()


@notion_prop("タスク種別")
class TaskKind(Select):
    def to_enum(self) -> TaskKindType:
        return TaskKindType(self.selected_name)

    @staticmethod
    def trash() -> "TaskKind":
        return TaskKind.from_name(TaskKindType.TRASH.value)

    @staticmethod
    def thisweek() -> "TaskKind":
        return TaskKind.from_name(TaskKindType.THIS_WEEK.value)


@notion_prop("メモジャンル")
class MemoGenre(Select):
    @staticmethod
    def create(typ: MemoGenreType) -> "MemoGenre":
        return MemoGenre.from_name(typ.value)


@notion_prop("習慣トラッカー")
class HabitRelation(Relation):
    pass


@notion_database(DatabaseType.TASK.value)
class Task(BasePage):
    task_name: TaskName
    important_flag: ImportantFlag
    project_relation: ProjectRelation
    task_date: TaskStartDate
    status: TaskStatus
    kind: TaskKind
    memo_genre: MemoGenre
    habit_relation: HabitRelation

    def update_status(self, status: TaskStatusType) -> "Task":
        self.set_prop(TaskStatus.from_status_type(status))
        return self

    def update_start_datetime(
        self,
        start: datetime | date | None = None,
        end: datetime | date | None = None,
    ) -> "Task":
        self.set_prop(TaskStartDate.from_range(start, end))
        return self

    def do_tomorrow(self) -> "Task":
        start_date = self.task_date.start_date
        if start_date is not None:
            self.set_prop(TaskStartDate.from_start_date(start_date + timedelta(days=1)))
        return self

    def start(self) -> "Task":
        start = jst_now()
        end = start + timedelta(minutes=30)
        return self.update_status(TaskStatusType.IN_PROGRESS).update_start_datetime(start, end)

    def complete(self) -> "Task":
        return self.update_status(TaskStatusType.DONE).update_end_datetime(end=jst_now())

    def update_end_datetime(self, end: datetime) -> "Task":
        """タスクの終了日時を更新する"""
        start = self.task_date.start_time
        if start is None:
            # 開始時刻がない場合はなにもしない
            return self
        self.set_prop(TaskStartDate.from_range(start, end))
        return self

    def add_check_prefix(self) -> "Task":
        rich_text = RichTextBuilder.create().add_text("✔️").add_rich_text(self.task_name.rich_text).build()
        self.set_prop(TaskName.from_rich_text(rich_text))
        return self

    def to_backup_task(self) -> TaskBackup:
        return TaskBackup.generate(
            task_name=self.task_name,
            project_relation=self.project_relation,
            task_date=self.task_date,
            block_children=self.block_children,
        )

    @property
    def is_completed(self) -> bool:
        return self.status.is_done()

    @property
    def start_datetime(self) -> datetime | None:
        return self.task_date.start_datetime

    @property
    def start_date(self) -> date | datetime | None:
        return self.task_date.start_time

    @property
    def end_datetime(self) -> datetime | None:
        return self.task_date.end_datetime

    def is_next_action(self) -> bool:
        return self.kind.to_enum() == TaskKindType.NEXT_ACTION

    def is_scheduled(self) -> bool:
        return self.kind.to_enum() == TaskKindType.SCHEDULE

    @property
    def order(self) -> int:
        return TaskOrderRule.calculate(
            start_datetime=self.start_datetime,
            kind=self.kind.to_enum(),
        ).value
