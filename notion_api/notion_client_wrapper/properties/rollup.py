from dataclasses import dataclass
from notion_client_wrapper.properties.property import Property
from typing import Optional


@dataclass
class Rollup(Property):
    rollup_type: str
    rollup_value: str
    rollup_function: str
    type: str = "rollup"


    def __init__(self, name: str, rollup_type: str, rollup_value: str, rollup_function: str, id: Optional[str] = None):
        self.name = name
        self.id = id
        self.rollup_type = rollup_type
        self.rollup_value = rollup_value
        self.rollup_function = rollup_function


    @staticmethod
    def of(name: str, param: dict) -> "Rollup":
        rollup_param = param["rollup"]
        if rollup_param["type"] != "number":
            raise NotImplementedError(f"Unsupported rollup type: {rollup_param['type']}")
        return Rollup(
            name=name,
            id=param["id"],
            rollup_type=rollup_param["type"],
            rollup_value=rollup_param["number"],
            rollup_function=rollup_param["function"]
        )

    def __dict__(self):
        return {
            "id": self.id,
            "type": self.type,
            "rollup": {
                "type": self.rollup_type,
                self.rollup_type: self.rollup_value,
                "function": self.rollup_function
            },
        }
