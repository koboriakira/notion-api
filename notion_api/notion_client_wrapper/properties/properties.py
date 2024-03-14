from dataclasses import dataclass

from notion_client_wrapper.properties.property import Property
from notion_client_wrapper.properties.title import Title


@dataclass(frozen=True)
class Properties:
    values: list[Property]

    def __dict__(self):
        result = {}
        for value in self.values:
            result = {**result, **value.__dict__()}
        return result

    @staticmethod
    def from_dict(properties: dict[str, dict]) -> "Properties":
        values = []
        for key, value in properties.items():
            values.append(Property.from_dict(key, value))
        return Properties(values=values)

    def get_title(self) -> Title:
        for value in self.values:
            if isinstance(value, Title):
                return value
        raise Exception(f"Title property not found. properties: {self.values}")

    def get_property(self, name: str, instance_class: type) -> Property | None:
        for value in self.values:
            if isinstance(value, instance_class) and value.name == name:
                return value
        return None
