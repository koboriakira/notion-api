from dataclasses import dataclass
from notion_client_wrapper.properties.property import Property
from typing import Optional


@dataclass
class Number(Property):
    number: Optional[int]
    type: str = "number"

    def __init__(self, name: str, id: Optional[str] = None, number: Optional[int] = None):
        self.name = name
        self.id = id
        self.number = number

    def add(self, count: int) -> "Number":
        prev = self.number if self.number is not None else 0
        return Number(
            name=self.name,
            id=self.id,
            number=prev + count
        )

    @staticmethod
    def of(name: str, param: dict) -> "Number":
        if param["number"] is None:
            return Number(name=name, id=param["id"])
        return Number(
            name=name,
            id=param["id"],
            number=param["number"]
        )

    def __dict__(self):
        result = {
        }
        if self.id is not None:
            result["id"] = self.id
        if self.number is not None:
            result["type"] = self.type
            result["number"] = self.number
        return {
            self.name: result
        }

    @ staticmethod
    def from_num(name: str, value: int) -> "Number":
        return Number(
            name=name,
            number=value
        )
