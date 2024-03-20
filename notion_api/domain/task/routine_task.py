from dataclasses import dataclass
from datetime import date

from domain.task.routine_kind import RoutineKind, RoutineType
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.title import Title
from util.datetime import jst_today

COLUMN_NAME_TITLE = "名前"

@dataclass
class RoutineTask(BasePage):
    @staticmethod
    def create(title: str, routine_type: RoutineType) -> "RoutineTask":
        title_property = Title.from_plain_text(name=COLUMN_NAME_TITLE, text=title)
        routine_kind = RoutineKind.create(routine_type)
        return RoutineTask(
            properties=Properties(values=[title_property, routine_kind]),
            block_children=[])

    def get_routine_type(self) -> RoutineType:
        routine_kind = self.get_select(name=RoutineKind.NAME)
        if routine_kind is None:
            msg = f"RoutineKind が見つかりません: {self}"
            raise ValueError(msg)
        return RoutineType.from_text(routine_kind.selected_name)

    def get_next_date(self) -> date:
        basis_date = jst_today()
        return self.get_routine_type().next_date(basis_date)
