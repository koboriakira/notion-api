from dataclasses import dataclass
from datetime import date, datetime, time

from lotion.base_page import BasePage
from task.domain.rouitne_option import RoutineOption
from task.domain.routine_kind import RoutineKind, RoutineType
from task.domain.task_context import TaskContextType, TaskContextTypes
from util.datetime import JST, jst_today

COLUMN_NAME_TITLE = "名前"


@dataclass
class RoutineTask(BasePage):
    def get_routine_type(self) -> RoutineType:
        routine_kind = self.get_select(name=RoutineKind.NAME)
        if routine_kind is None:
            msg = f"RoutineKind が見つかりません: {self}"
            raise ValueError(msg)
        return RoutineType.from_text(routine_kind.selected_name)

    def get_next_date(self, basis_date:date|None = None) -> date:
        basis_date = jst_today() if basis_date is None else basis_date
        return self.get_routine_type().next_date(basis_date)

    def get_next_schedule(self, basis_date:date|None = None) -> tuple[datetime, datetime|None]:
        next_date = self.get_next_date(basis_date=basis_date)
        routine_time = self.get_text(name="時間")
        if routine_time is None or routine_time.text == "":
            return datetime.combine(next_date, datetime.min.time(), JST), None
        start_time_text, end_time_text = routine_time.text.split("-")
        start_time = time.fromisoformat(start_time_text)
        end_time = time.fromisoformat(end_time_text)
        start_datetime = datetime.combine(next_date, start_time, JST)
        end_datetime = datetime.combine(next_date, end_time, JST) if end_time is not None else None
        return start_datetime, end_datetime

    def due_time(self) -> time | None:
        due_time_text = self.get_text(name="締め切り")
        if due_time_text is None:
            return None
        try:
            return time.fromisoformat(due_time_text.text)
        except ValueError:
            return None

    def get_contexts(self) -> TaskContextTypes:
        routine_option = self.get_text(name=RoutineOption.NAME)
        if routine_option is None or routine_option.text == "":
            return TaskContextTypes(values=[])
        task_context_type_list = [TaskContextType.from_text(text) for text in routine_option.text.split(",")]
        return TaskContextTypes(values=task_context_type_list)
