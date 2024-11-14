from enum import Enum

from notion_client_wrapper.properties.select import Select

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

    @staticmethod
    def from_text(text: str) -> "TaskKindType":
        for kind_type in TaskKindType:
            if kind_type.value == text:
                return kind_type
        msg = f"TaskKindType に存在しない値です: {text}"
        raise ValueError(msg)

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

    @property
    def selected_name(self) -> str:
        return self.value

    @property
    def selected_id(self) -> str:
        return kind_map[self.value]["selected_id"]

    @property
    def selected_color(self) -> str:
        return kind_map[self.value]["selected_color"]


class TaskKind(Select):
    NAME = "タスク種別"

    def __init__(self, kind_type: TaskKindType) -> None:
        super().__init__(
            name=self.NAME,
            selected_name=kind_type.selected_name,
            selected_id=kind_type.selected_id,
            selected_color=kind_type.selected_color,
            id=None,
        )

    @classmethod
    def create(cls, kind_type: TaskKindType) -> "TaskKind":
        return cls(kind_type=kind_type)

    @classmethod
    def trash(cls) -> "TaskKind":
        return cls.create(kind_type=TaskKindType.TRASH)

    @classmethod
    def routine(cls) -> "TaskKind":
        return cls.create(kind_type=TaskKindType.ROUTINE)

    @classmethod
    def scheduled(cls) -> "TaskKind":
        return cls.create(kind_type=TaskKindType.SCHEDULE)

if __name__ == "__main__":
    # 最新の情報を取得するときに使う
    # python -m notion_api.task.domain.task_kind
    from common.value.database_type import DatabaseType
    from notion_client_wrapper.client_wrapper import ClientWrapper

    # python -m notion_api.task.domain.task_context
    pages = ClientWrapper.get_instance().retrieve_database(
        database_id=DatabaseType.TASK.value,
    )

    result = {}
    for page in pages:
        select_property = page.get_select(name=TaskKind.NAME)
        if select_property is None:
            continue
        if select_property.selected_id in result:
            continue
        result[select_property.selected_name] = {
            "selected_id": select_property.selected_id,
            "selected_color": select_property.selected_color,
        }
    # uniqueにする
    import json

    print(json.dumps(result, ensure_ascii=False))
