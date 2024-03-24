from notion_client_wrapper.filter.condition.condition import Condition
from notion_client_wrapper.filter.condition.string_condition import StringCondition
from notion_client_wrapper.properties.property import Property


class FilterBuilder:
    def __init__(self, conditions: list[Condition]|None = None) -> None:
        self.conditions = conditions or []

    def add_condition(self, condition: StringCondition) -> "FilterBuilder":
        return FilterBuilder(conditions=[*self.conditions, condition])

    @staticmethod
    def build_simple_equal_condition(property: Property) -> dict:  # noqa: A002
        result = FilterBuilder().add_condition(StringCondition.equal(property=property)).build()
        if result is None:
            msg = "Filter is empty"
            raise ValueError(msg)
        return result

    def build(self) -> dict|None:
        if len(self.conditions) == 0:
            return None
        if len(self.conditions) == 1:
            return self.conditions[0].__dict__()
        return {
            "and": [condition.__dict__() for condition in self.conditions],
        }
