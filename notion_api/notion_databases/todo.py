from curses import intrflush
from datetime import timedelta
from enum import Enum
import stat

from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.properties import Date, Status, Title, Select, Relation

from common.value.database_type import DatabaseType
from util.datetime import jst_now, jst_today


class TodoStatusEnum(Enum):
    """タスクのステータス"""

    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TodoKindEnum(Enum):
    SCHEDULE = "スケジュール"
    PROJECT = "プロジェクト"
    REPEAT = "リピート"
    INTERRUPTION = "差し込み"
    SINGLE = "単発"
    SUBTASK = "サブタスク"


class TodoSectionEnum(Enum):
    A_07_10 = "A_07_10"
    B_10_13 = "B_10_13"
    C_13_15 = "C_13_15"
    D_15_17 = "D_15_17"
    E_17_20 = "E_17_20"
    F_20_22 = "F_20_22"
    G_22_24 = "G_23_07"


@notion_prop("名前")
class TodoName(Title):
    pass

@notion_prop("ステータス")
class TodoStatus(Status):
    @staticmethod
    def from_status_type(status_type: TodoStatusEnum) -> "TodoStatus":
        return TodoStatus.from_status_name(status_type.value)

    @staticmethod
    def inprogress() -> "TodoStatus":
        return TodoStatus.from_status_name(TodoStatusEnum.IN_PROGRESS.value)

@notion_prop("タスク種別")
class TodoKind(Select):
    @staticmethod
    def from_kind_type(kind_type: TodoKindEnum) -> "TodoKind":
        return TodoKind.from_name(kind_type.value)

    @staticmethod
    def from_enum(kind_enum: TodoKindEnum) -> "TodoKind":
        return TodoKind.from_name(kind_enum.value)


@notion_prop("セクション")
class TodoSection(Select):
    @staticmethod
    def from_section_type(section_type: TodoSectionEnum) -> "TodoSection":
        return TodoSection.from_name(section_type.value)

@notion_prop("実施期間")
class TodoLogDate(Date):
    pass


@notion_prop("サブタスク")
class TodoSubtask(Relation):
    pass


@notion_prop("親タスク")
class TodoParentTask(Relation):
    pass



@notion_database(DatabaseType.TODO_LIST.value)
class Todo(BasePage):
    name: TodoName
    status: TodoStatus
    kind: TodoKind
    section: TodoSection
    log_date: TodoLogDate
    subtask: TodoSubtask
    parent_task: TodoParentTask


    def todo(self) -> "Todo":
        """未実施状態に変更して返す"""
        self.status = TodoStatus.from_status_type(TodoStatusEnum.TODO)
        return self

    def inprogress(self) -> "Todo":
        """進行中状態に変更して返す"""
        self.status = TodoStatus.from_status_type(TodoStatusEnum.IN_PROGRESS)
        self.log_date = TodoLogDate.from_start_date(jst_now())
        return self

    def complete(self) -> "Todo":
        """完了状態に変更して返す"""
        self.status = TodoStatus.from_status_type(TodoStatusEnum.DONE)
        self.log_date = TodoLogDate.from_range(
            start=self.log_date.start_datetime or jst_now(),
            end=jst_now(),
        )
        return self

    def is_sub_task(self) -> bool:
        """サブタスクかどうか"""
        return self.get_formula("サブタスク判定")._formula["boolean"]
