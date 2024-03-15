from dataclasses import dataclass

from notion_client_wrapper.properties.property import Property


@dataclass(frozen=True)
class MultiSelectElement:
    id: str
    name: str
    color: str

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
        }


@dataclass
class MultiSelect(Property):
    values: list[MultiSelectElement]
    type: str = "multi_select"

    def __init__(
            self,
            name: str,
            values: list[dict[str, str]],
            id: str | None = None) -> None:  # noqa: A002
        self.name = name
        self.values = values
        self.id = id

    @ staticmethod
    def of(name: str, param: dict) -> "MultiSelect":
        multi_select = [
            MultiSelectElement(
                id=element["id"],
                name=element["name"],
                color=element["color"],
            ) for element in param["multi_select"]]

        return MultiSelect(
            name=name,
            values=multi_select,
            id=param["id"],
        )

    def __dict__(self) -> dict:
        result = [e.__dict__() for e in self.values]
        return {self.name: result}

    def value_for_filter(self) -> str:
        raise NotImplementedError
