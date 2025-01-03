from dataclasses import dataclass
from enum import Enum


class TaskContextType(Enum):
    CONSENTRATION = "集中"
    TWO_MINUTES = "2分で終わる"
    GO_OUT = "外出"

    @staticmethod
    def from_text(text: str) -> "TaskContextType":
        for kind in TaskContextType:
            if kind.value == text:
                return kind
        raise ValueError(f"Invalid TaskContextType: {text}")


@dataclass(frozen=True)
class TaskContextTypes:
    values: list[TaskContextType]

    def __post_init__(self) -> None:
        for value in self.values:
            if not isinstance(value, TaskContextType):
                msg = f"[{type(self)} Invalid type for {value}: {type(value)}"
                raise TypeError(msg)

    def to_str_list(self) -> list[str]:
        return [kind.name for kind in self.values]
