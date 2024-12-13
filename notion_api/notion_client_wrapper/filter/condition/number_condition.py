from dataclasses import dataclass
from enum import Enum

from lotion.properties import Property

from .condition import Condition


class NumberConditionType(Enum):
    EQUALS= "equals"

@dataclass(frozen=True)
class NumberCondition(Condition):
    property_name: str
    property_type: str
    condition_type: NumberConditionType
    value: str

    @staticmethod
    def equal(property: Property) -> "NumberCondition":
        return NumberCondition(
            property_name=property.name,
            property_type=property.type,
            condition_type=NumberConditionType.EQUALS,
            value=property.value_for_filter(),
        )

    def __dict__(self) -> dict:
        return {
            "property": self.property_name,
            self.property_type: {
                self.condition_type.value: self.value,
            },
        }
