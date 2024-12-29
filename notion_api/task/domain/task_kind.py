from enum import Enum

from lotion.properties import Select

kind_map = {
    "次にとるべき行動リスト": {"selected_id": "d73dbc77-702d-4b2e-88e1-22b54a17a333", "selected_color": "brown"},
    "スケジュール": {"selected_id": "a6e6329d-f547-44d4-b418-ac239dd88632", "selected_color": "blue"},
    "ルーティン": {"selected_id": "44c37655-c056-49d2-8441-61929400f6a3", "selected_color": "default"},
    "今すぐやる": {"selected_id": "a0cab03e-aa5c-4619-835b-7f1cedd6500f", "selected_color": "pink"},
    "ゴミ箱": {"selected_id": "e4179710-03ef-43c0-8fb3-01b463e25edd", "selected_color": "purple"},
    "待ち": {"selected_id": "8c1685c7-5398-4cea-b950-b874501a7713", "selected_color": "gray"},
    "いつかやる・たぶんやる": {"selected_id": "66d35bb2-7f64-41d3-8ec8-48f025e47236", "selected_color": "orange"},
}


class TaskKindType(Enum):
    TRASH = "ゴミ箱"
    WAIT = "待ち"
    DO_NOW = "今すぐやる"
    NEXT_ACTION = "次にとるべき行動リスト"
    SOMEDAY_MAYBE = "いつかやる・たぶんやる"
    SCHEDULE = "スケジュール"
    ROUTINE = "ルーティン"

    @property
    def priority(self) -> int:
        return {
            TaskKindType.TRASH: 0,
            TaskKindType.ROUTINE: 1,
            TaskKindType.WAIT: 2,
            TaskKindType.SOMEDAY_MAYBE: 3,
            TaskKindType.SCHEDULE: 4,
            TaskKindType.NEXT_ACTION: 5,
            TaskKindType.DO_NOW: 6,
        }[self]


