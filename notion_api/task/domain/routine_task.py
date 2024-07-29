from dataclasses import dataclass
from datetime import date, time

from notion_client_wrapper.base_page import BasePage
from task.domain.rouitne_option import RoutineOption
from task.domain.routine_kind import RoutineKind, RoutineType
from task.domain.task_context import TaskContextType, TaskContextTypes
from util.datetime import jst_today

COLUMN_NAME_TITLE = "名前"


@dataclass
class RoutineTask(BasePage):
    def get_routine_type(self) -> RoutineType:
        routine_kind = self.get_select(name=RoutineKind.NAME)
        if routine_kind is None:
            msg = f"RoutineKind が見つかりません: {self}"
            raise ValueError(msg)
        return RoutineType.from_text(routine_kind.selected_name)

    def get_next_date(self) -> date:
        basis_date = jst_today()
        return self.get_routine_type().next_date(basis_date)

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
