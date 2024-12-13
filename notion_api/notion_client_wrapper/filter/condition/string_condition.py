from dataclasses import dataclass
from enum import Enum

from lotion.properties import Property

from .condition import Condition


class StringConditionType(Enum):
    EQUALS= "equals"
    NOT_EQUAL = "does_not_equal"

@dataclass(frozen=True)
class StringCondition(Condition):
    property_name: str
    property_type: str
    condition_type: StringConditionType
    value: str

    @staticmethod
    def equal(property: Property) -> "StringCondition":
        return StringCondition._from_property(property, StringConditionType.EQUALS)

    @staticmethod
    def not_equal(property: Property) -> "StringCondition":
        return StringCondition._from_property(property, StringConditionType.NOT_EQUAL)

    @staticmethod
    def _from_property(property: Property, condition_type: StringConditionType) -> "StringCondition":
        return StringCondition(
            property_name=property.name,
            property_type=property.type,
            condition_type=condition_type,
            value=property.value_for_filter(),
        )

    def __dict__(self) -> dict:
        return {
            "property": self.property_name,
            self.property_type: {
                self.condition_type.value: self.value,
            },
        }
