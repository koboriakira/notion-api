from dataclasses import dataclass
from enum import Enum

from notion_client_wrapper.properties.property import Property

from .condition import Condition


class EmptyConditionType(Enum):
    IS_EMPTY = "is_empty"
    IS_NOT_EMPTY = "is_not_empty"


@dataclass(frozen=True)
class EmptyCondition(Condition):
    prop_name: str
    prop_type: str
    condition_type: EmptyConditionType

    @classmethod
    def true(cls: "EmptyCondition", property: Property) -> "EmptyCondition":  # noqa: A002
        return cls(
            prop_name=property.name,
            prop_type=property.type,
            condition_type=EmptyConditionType.IS_EMPTY,
        )

    @classmethod
    def false(cls: "EmptyCondition", property: Property) -> "EmptyCondition":  # noqa: A002
        return cls(
            prop_name=property.name,
            prop_type=property.type,
            condition_type=EmptyConditionType.IS_NOT_EMPTY,
        )

    def __dict__(self) -> dict:
        return {
            "property": self.prop_name,
            self.prop_type: {
                self.condition_type.value: True,
            },
        }
