from dataclasses import dataclass

from lotion.properties import MultiSelect
from lotion.properties.multi_select import MultiSelectElement

KIND_LIST = [
    {"name": "集中", "id": "69615ccf-b98e-4764-b4a7-8cc920e03d92"},
    {"name": "2分で終わる", "id": "e7cb77c6-7d3e-4270-8102-5d23f881382f"},
    {"name": "外出", "id": "c455b93b-dfa8-4e69-bff8-664db9c669ff"},
]


@dataclass(frozen=True)
class TaskContextType:
    name: str
    id: str

    @staticmethod
    def from_text(text: str) -> "TaskContextType":
        for kind_type in KIND_LIST:
            if kind_type["name"] == text:
                return TaskContextType(**kind_type)
        msg = f"TaskContextType に存在しない値です: {text}"
        raise ValueError(msg)

    def __dict__(self) -> dict[str, str]:
        return {"name": self.name, "id": self.id}

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, TaskContextType):
            return False
        return self.id == __value.id


@dataclass(frozen=True)
class TaskContextTypes:
    values: list[TaskContextType]

    def __post_init__(self) -> None:
        for value in self.values:
            if not isinstance(value, TaskContextType):
                msg = f"[{type(self)} Invalid type for {value}: {type(value)}"
                raise TypeError(msg)

    def to_multi_select_elements(self) -> list[MultiSelectElement]:
        return [MultiSelectElement(**kind.__dict__()) for kind in self.values]

    def to_str_list(self) -> list[str]:
        return [kind.name for kind in self.values]


class TaskContext(MultiSelect):
    NAME = "コンテクスト"

    def __init__(self, kind_types: TaskContextTypes) -> None:
        super().__init__(
            name=self.NAME,
            values=kind_types.to_multi_select_elements(),
        )


if __name__ == "__main__":
    # 最新の情報を取得するときに使う
    # python -m notion_api.task.domain.task_context
    from lotion import Lotion

    from common.value.database_type import DatabaseType

    pages = Lotion.get_instance().retrieve_database(
        database_id=DatabaseType.TASK.value,
    )

    result = []
    for page in pages:
        select_property = page.get_multi_select(name="コンテクスト")
        if select_property is None:
            continue
        values = select_property.values
        result.extend([{"name": value.name, "id": value.id} for value in values])
    # uniqueにする
    result = list({value["name"]: value for value in result}.values())
    import json

    print(json.dumps(result, ensure_ascii=False))
