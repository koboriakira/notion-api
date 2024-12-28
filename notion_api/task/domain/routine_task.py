from datetime import date, datetime, time

from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.properties import Property, Select, Text, Title

from common.value.database_type import DatabaseType
from task.domain.routine_kind import RoutineType
from task.domain.task_context import TaskContextType, TaskContextTypes
from util.datetime import JST, jst_today


@notion_prop("名前")
class RoutineTitle(Title):
    pass


@notion_prop("オプション")
class RoutineOption(Text):
    pass


@notion_prop("時間")
class RoutineTime(Text):
    pass


@notion_prop("周期")
class RoutineKind(Select):
    pass


@notion_database(DatabaseType.TASK_ROUTINE.value)
class RoutineTask(BasePage):
    title: RoutineTitle
    option: RoutineOption
    routine_time: RoutineTime
    kind: RoutineKind

    def get_routine_type(self) -> RoutineType:
        return RoutineType.from_text(self.kind.selected_name)

    def get_next_date(self, basis_date: date | None = None) -> date:
        basis_date = jst_today() if basis_date is None else basis_date
        return self.get_routine_type().next_date(basis_date)

    def get_next_schedule(self, basis_date: date | None = None) -> tuple[datetime, datetime | None]:
        next_date = self.get_next_date(basis_date=basis_date)
        if self.routine_time.text == "":
            return datetime.combine(next_date, datetime.min.time(), JST), None
        start_time_text, end_time_text = self.routine_time.text.split("-")
        start_time = time.fromisoformat(start_time_text)
        end_time = time.fromisoformat(end_time_text)
        start_datetime = datetime.combine(next_date, start_time, JST)
        end_datetime = datetime.combine(next_date, end_time, JST) if end_time is not None else None
        return start_datetime, end_datetime

    def get_contexts(self) -> TaskContextTypes:
        if self.option.text == "":
            return TaskContextTypes(values=[])
        task_context_type_list = [TaskContextType.from_text(text) for text in self.option.text.split(",")]
        return TaskContextTypes(values=task_context_type_list)

    @staticmethod
    def generate(title: str) -> "RoutineTask":
        properties: list[Property] = []
        properties.append(RoutineTitle.from_plain_text(title))
        return RoutineTask.create(properties)
