from dataclasses import dataclass
from enum import Enum

from notion_client_wrapper.properties.checkbox import Checkbox

from .condition import Condition


class CheckboxConditionType(Enum):
    EQUALS = "equals"
    NOT_EQUAL = "does_not_equal"


@dataclass(frozen=True)
class CheckboxCondition(Condition):
    property_name: str
    condition_type: CheckboxConditionType
    value: bool
    # "checkbox"のみなので、property_typeは不要

    @staticmethod
    def equal(_property: Checkbox) -> "CheckboxCondition":
        return CheckboxCondition._from_property(_property, CheckboxConditionType.EQUALS)

    @staticmethod
    def not_equal(_property: Checkbox) -> "CheckboxCondition":
        return CheckboxCondition._from_property(_property, CheckboxConditionType.NOT_EQUAL)

    @staticmethod
    def _from_property(_property: Checkbox, condition_type: CheckboxConditionType) -> "CheckboxCondition":
        return CheckboxCondition(
            property_name=_property.name,
            condition_type=condition_type,
            value=_property.checked,
        )

    def __dict__(self) -> dict:
        return {
            "property": self.property_name,
            "checkbox": {
                self.condition_type.value: self.value,
            },
        }
