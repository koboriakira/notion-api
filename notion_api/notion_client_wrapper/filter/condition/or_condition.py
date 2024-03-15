from dataclasses import dataclass

from .condition import Condition


@dataclass(frozen=True)
class OrCondition(Condition):
    conditions: list[Condition]

    @staticmethod
    def create(*conditions: Condition) -> "OrCondition":
        return OrCondition(conditions=list(conditions))


    def __dict__(self) -> dict:
        return {
            "or": [c.__dict__() for c in self.conditions],
        }
