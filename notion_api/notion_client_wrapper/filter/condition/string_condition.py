from dataclasses import dataclass
from enum import Enum

from notion_api.notion_client_wrapper.properties.property import Property

from .condition import Condition


class StringConditionType(Enum):
    EQUALS= "equals"

@dataclass(frozen=True)
class StringCondition(Condition):
    property_name: str
    property_type: str
    condition_type: StringConditionType
    value: str

    @staticmethod
    def equal(property: Property) -> "StringCondition":
        return StringCondition(
            property_name=property.name,
            property_type=property.type,
            condition_type=StringConditionType.EQUALS,
            value=property.value_for_filter(),
        )

    def __dict__(self) -> dict:
        return {
            "property": self.property_name,
            self.property_type: {
                self.condition_type.value: self.value,
            },
        }
