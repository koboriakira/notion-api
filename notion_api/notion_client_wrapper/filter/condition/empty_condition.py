from dataclasses import dataclass
from enum import Enum

from notion_client_wrapper.properties.property import Property

from .condition import Condition


class EmptyConditionType(Enum):
    IS_EMPTY= "is_empty"
    IS_NOT_EMPTY = "is_not_empty"

@dataclass(frozen=True)
class EmptyCondition(Condition):
    property_name: str
    property_type: str
    condition_type: EmptyConditionType

    @staticmethod
    def true(property: Property) -> "EmptyCondition":  # noqa: A002
        return EmptyCondition._from_property(property, EmptyConditionType.IS_EMPTY)

    @staticmethod
    def false(property: Property) -> "EmptyCondition":  # noqa: A002
        return EmptyCondition._from_property(property, EmptyConditionType.IS_NOT_EMPTY)

    @staticmethod
    def _from_property(property: Property, condition_type: EmptyConditionType) -> "EmptyCondition":
        return EmptyCondition(
            property_name=property.name,
            property_type=property.type,
            condition_type=condition_type,
        )

    def __dict__(self) -> dict:
        return {
            "property": self.property_name,
            self.property_type: {
                self.condition_type.value: True,
            },
        }
