from dataclasses import dataclass

from notion_client_wrapper.properties.property import Property


@dataclass(frozen=True)
class MultiSelectElement:
    id: str
    name: str
    color: str | None = None

    def __dict__(self) -> dict:
        result = {
            "id": self.id,
            "name": self.name,
        }
        if self.color:
            result["color"] = self.color
        return result


@dataclass
class MultiSelect(Property):
    values: list[MultiSelectElement]
    type: str = "multi_select"

    def __init__(self, name: str, values: list[MultiSelectElement], id: str | None = None) -> None:  # noqa: A002
        self.name = name
        self.values = values
        self.id = id

    def __post_init__(self) -> None:
        if not all(isinstance(value, MultiSelectElement) for value in self.values):
            raise ValueError("All values must be MultiSelectElement instances.")

    @staticmethod
    def of(name: str, param: dict) -> "MultiSelect":
        multi_select = [
            MultiSelectElement(
                id=element["id"],
                name=element["name"],
                color=element["color"],
            )
            for element in param["multi_select"]
        ]

        return MultiSelect(
            name=name,
            values=multi_select,
            id=param["id"],
        )

    @staticmethod
    def create(name: str, values: list[dict[str, str]]) -> "MultiSelect":
        """
        Create a MultiSelect instance from a list of dictionaries.

        Args:
            name (str): Name of the property.
            values (list[dict[str, str]]): List of dictionaries. Each dictionary should have keys "id" and "name".

        Returns:
            MultiSelect: MultiSelect instance.
        """
        multi_select = [MultiSelectElement(id=element["id"], name=element["name"]) for element in values]
        return MultiSelect(
            name=name,
            values=multi_select,
        )

    def __dict__(self) -> dict:
        result = [e.__dict__() for e in self.values]
        return {self.name: result}

    def value_for_filter(self) -> str:
        raise NotImplementedError
