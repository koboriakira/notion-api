from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from lotion.properties import Property

from .condition import Condition


class DateConditionType(Enum):
    EQUALS = "equals"
    ON_OR_AFTER = "on_or_after"
    ON_OR_BEFORE = "on_or_before"
    BEFORE = "before"


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

    @staticmethod
    def on_or_after(property: Property) -> "DateCondition":
        return DateCondition(
            property_name=property.name,
            property_type=property.type,
            condition_type=DateConditionType.ON_OR_AFTER,
            value=property.value_for_filter(),
        )

    @staticmethod
    def create_manually(name: str, condition_type: DateConditionType, value: datetime) -> "DateCondition":
        return DateCondition(
            property_name=name,
            property_type="date",
            condition_type=condition_type,
            value=value.isoformat(),
        )

    @staticmethod
    def before(property: Property) -> "DateCondition":
        return DateCondition(
            property_name=property.name,
            property_type=property.type,
            condition_type=DateConditionType.BEFORE,
            value=property.value_for_filter(),
        )

    @staticmethod
    def on_or_before(property: Property) -> "DateCondition":
        return DateCondition(
            property_name=property.name,
            property_type=property.type,
            condition_type=DateConditionType.ON_OR_BEFORE,
            value=property.value_for_filter(),
        )

    def __dict__(self) -> dict:
        return {
            "property": self.property_name,
            self.property_type: {
                self.condition_type.value: self.value,
            },
        }
