from datetime import date, datetime, time

from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.properties import Property, Select, Text, Title

from common.value.database_type import DatabaseType
from notion_databases.routine_prop.routine_type import RoutineType
from util.datetime import JST, jst_today


@notion_prop("名前")
class RoutineTitle(Title):
    pass


@notion_prop("時間")
class RoutineTime(Text):
    pass


@notion_prop("周期")
class RoutineKind(Select):
    def to_enum(self) -> RoutineType:
        return RoutineType.from_text(self.selected_name)


@notion_database(DatabaseType.TASK_ROUTINE.value)
class RoutineTask(BasePage):
    title: RoutineTitle
    routine_time: RoutineTime
    kind: RoutineKind

    def get_routine_type(self) -> RoutineType:
        return self.kind.to_enum()

    def get_next_date(self, basis_date: date | None = None) -> date:
        basis_date = jst_today() if basis_date is None else basis_date
        return self.get_routine_type().next_date(basis_date)

    def get_next_schedule(self, basis_date: date | None = None) -> tuple[date | datetime, datetime | None]:
        next_date = self.get_next_date(basis_date=basis_date)
        if self.routine_time.text == "":
            return next_date, None
        start_time_text, end_time_text = self.routine_time.text.split("-")
        start_time = time.fromisoformat(start_time_text)
        end_time = time.fromisoformat(end_time_text)
        start_datetime = datetime.combine(next_date, start_time, JST)
        end_datetime = datetime.combine(next_date, end_time, JST) if end_time is not None else None
        return start_datetime, end_datetime

    @staticmethod
    def generate(title: str) -> "RoutineTask":
        properties: list[Property] = []
        properties.append(RoutineTitle.from_plain_text(title))
        return RoutineTask.create(properties)
