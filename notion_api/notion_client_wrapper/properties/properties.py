from dataclasses import dataclass

from notion_client_wrapper.properties.property import Property
from notion_client_wrapper.properties.title import Title


@dataclass(frozen=True)
class Properties:
    values: list[Property]

    def __post_init__(self) -> None:
        for value in self.values:
            if not isinstance(value, Property):
                msg = f"values must be Property. value: {value}"
                raise TypeError(msg)

    def __dict__(self) -> dict:
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

    def append_property(self, prop: Property) -> "Properties":
        props = []

        for original_prop in self.values:
            if original_prop is None:
                # この場合があるらしい。どこかで混じったかな?
                continue
            if prop.name == original_prop.name:
                props.append(prop)
            else:
                props.append(original_prop)

        return Properties(values=props)

    def get_title(self) -> Title:
        for value in self.values:
            if isinstance(value, Title):
                return value
        msg = f"Title property not found. properties: {self.values}"
        raise Exception(msg)

    def get_property(self, name: str, instance_class: type) -> Property | None:
        for value in self.values:
            if isinstance(value, instance_class) and value.name == name:
                return value
        return None

    def exclude_button(self) -> "Properties":
        """
        ボタンのプロパティは更新時にエラーとなるため、除外する。
        """
        return Properties(values=[prop for prop in self.values if prop.type != "button"])

    def is_empty(self) -> bool:
        return len(self.values) == 0
