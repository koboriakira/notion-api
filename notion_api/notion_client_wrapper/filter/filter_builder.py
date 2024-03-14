from notion_client_wrapper.filter.condition.condition import Condition
from notion_client_wrapper.filter.condition.string_condition import StringCondition


class FilterBuilder:
    def __init__(self, conditions: list[Condition]|None = None) -> None:
        self.conditions = conditions or []

    def add_condition(self, condition: StringCondition) -> "FilterBuilder":
        return FilterBuilder(conditions=[*self.conditions, condition])

    def build(self) -> dict|None:
        if len(self.conditions) == 0:
            return None
        if len(self.conditions) == 1:
            return self.conditions[0].__dict__()
        return {
            "and": [condition.__dict__() for condition in self.conditions],
        }
