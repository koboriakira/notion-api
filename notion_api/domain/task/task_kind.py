from enum import Enum

from notion_client_wrapper.properties.select import Select

kind_map = {
    "ゴミ箱": "e4179710-03ef-43c0-8fb3-01b463e25edd",
    "待ち": "8c1685c7-5398-4cea-b950-b874501a7713",
    "今すぐやる": "a0cab03e-aa5c-4619-835b-7f1cedd6500f",
    "次にとるべき行動リスト": "d73dbc77-702d-4b2e-88e1-22b54a17a333",
    "いつかやる・たぶんやる": "66d35bb2-7f64-41d3-8ec8-48f025e47236",
}

class TaskKindType(Enum):
    TRASH = "ゴミ箱"
    WAIT = "待ち"
    DO_NOW = "今すぐやる"
    NEXT_ACTION = "次にとるべき行動リスト"
    SOMEDAY_MAYBE = "いつかやる・たぶんやる"

    @property
    def selected_name(self) -> str:
        return self.value

    @property
    def selected_id(self) -> str:
        return kind_map[self.value]


class TaskKind(Select):
    def __init__(self, name: str, kind_type: TaskKindType) -> None:
        super().__init__(
            name=name,
            selected_name=kind_type.selected_name,
            selected_id=kind_type.selected_id,
            selected_color=None,
            id=None,
        )

    @staticmethod
    def trash() -> "TaskKind":
        return TaskKind(name="タスク種別", kind_type=TaskKindType.TRASH)
