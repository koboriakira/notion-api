from datetime import date, datetime, timedelta

from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.block.rich_text import RichTextBuilder
from lotion.properties import Checkbox, Date, Relation, Title

from common.value.database_type import DatabaseType
from task.domain.task_kind import TaskKind, TaskKindType
from task.domain.task_status import TaskStatus, TaskStatusType
from task.valueobject.task_order_rule import TaskOrderRule
from util.datetime import convert_to_date_or_datetime, jst_now

COLUMN_NAME_TITLE = "名前"
COLUMN_NAME_STATUS = "ステータス"
COLUMN_NAME_START_DATE = "実施日"
COLUMN_NAME_KIND = "タスク種別"


@notion_prop("名前")
class TaskName(Title):
    pass


@notion_prop("重要")
class ImportantFlag(Checkbox):
    pass


@notion_prop("プロジェクト")
class ProjectRelation(Relation):
    pass


@notion_prop("実施日")
class TaskStartDate(Date):
    pass


# @notion_prop("ステータス")
# @notion_prop("タスク種別")
# @notion_prop("プロジェクト")
# @notion_prop("実施日")


@notion_database(DatabaseType.TASK.value)
class ToDoTask(BasePage):
    task_name: TaskName
    important_flag: ImportantFlag
    project_relation: ProjectRelation
    task_date: TaskStartDate

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
        start_datetime: datetime | date | None = None,
        end_datetime: datetime | date | None = None,
    ) -> "ToDoTask":
        start_date = TaskStartDate.from_range(start_datetime, end_datetime)  # type: ignore
        properties = self.properties.append_property(start_date)
        self.properties = properties
        return self

    def do_tomorrow(self) -> "ToDoTask":
        if self.start_date is not None:
            date_ = self.start_date.date() if isinstance(self.start_date, datetime) else self.start_date
            start_date = TaskStartDate.from_start_date(date_ + timedelta(days=1))
            self.properties = self.properties.append_property(start_date)
        return self

    def start(self) -> "ToDoTask":
        start = jst_now()
        end = start + timedelta(minutes=30)
        return self.update_status(TaskStatusType.IN_PROGRESS).update_start_datetime(start, end)

    def complete(self) -> "ToDoTask":
        return self.update_status(TaskStatusType.DONE).update_start_end_datetime(end=jst_now())

    def update_start_end_datetime(self, end: datetime) -> "ToDoTask":
        """タスクの終了日時を更新する"""
        start = self.start_datetime
        if start is None:
            # 開始時刻がない場合はなにもしない
            return self
        start_date = TaskStartDate.from_range(start, end)
        self.properties = self.properties.append_property(start_date)
        return self

    def add_check_prefix(self) -> "ToDoTask":
        title = self.get_title()
        original_rich_text = title.rich_text
        rich_text = RichTextBuilder.create().add_text("✔️").add_rich_text(original_rich_text).build()
        title_prop = Title.from_rich_text(name=title.name, rich_text=rich_text)
        self.properties = self.properties.append_property(title_prop)
        return self

    @property
    def status(self) -> TaskStatusType:
        status_name = self.get_status(name=TaskStatus.NAME).status_name
        return TaskStatusType(status_name)

    @property
    def is_completed(self) -> bool:
        return self.status.is_done()

    @property
    def start_datetime(self) -> datetime | None:
        if self.task_date.start is None:
            return None
        result = convert_to_date_or_datetime(value=self.task_date.start, cls=datetime)
        return result

    @property
    def start_date(self) -> date | datetime | None:
        if self.task_date.start is None:
            return None
        return convert_to_date_or_datetime(value=self.task_date.start)

    @property
    def end_datetime(self) -> datetime | None:
        if self.task_date.start is None:
            return None
        return convert_to_date_or_datetime(value=self.task_date.end, cls=datetime)

    @property
    def kind(self) -> TaskKindType | None:
        kind_model = self.get_select(name=TaskKind.NAME)
        if kind_model.selected_name == "":
            return None
        return TaskKindType(kind_model.selected_name)

    def is_scheduled(self) -> bool:
        return self.kind == TaskKindType.SCHEDULE

    @property
    def order(self) -> int:
        return TaskOrderRule.calculate(
            start_datetime=self.start_datetime,
            kind=self.kind,
        ).value


type Task = ToDoTask
