from dataclasses import dataclass
from enum import Enum

from notion_api.notion_client_wrapper.properties.property import Property

from .condition import Condition


class DateConditionType(Enum):
    EQUALS= "equals"

@dataclass(frozen=True)
class DateCondition(Condition):
    property_name: str
    property_type: str
    condition_type: DateConditionType
    value: str

    @staticmethod
    def equal(property: Property) -> "DateCondition":
        return DateCondition(
            property_name=property.name,
            property_type=property.type,
            condition_type=DateConditionType.EQUALS,
            value=property.value_for_filter(),
        )

    def __dict__(self) -> dict:
        return {
            "property": self.property_name,
            self.property_type: {
                self.condition_type.value: self.value,
            },
        }
