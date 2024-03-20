from dataclasses import dataclass
from enum import Enum


class RoutineType(Enum):
    DAILY = "毎日"
    EVERY_SAT = "毎週土"
    EVERY_TUE_AND_FRI = "毎週火・金"
    EVERY_WED = "毎週水"
    DAYS_AFTER_7 = "7日後"
    DAYS_AFTER_3 = "3日後"

    @staticmethod
    def from_text(text: str) -> "RoutineType":
        for routine_type in RoutineType:
            if routine_type.value == text:
                return routine_type
        msg = f"RoutineType not found: {text}"
        raise ValueError(msg)

@dataclass(frozen=True)
class RoutineTask:
    title: str
    routine_type: RoutineType

    @staticmethod
    def create(title: str, routine_type_text: str) -> "RoutineTask":
        return RoutineTask(
            title=title,
            routine_type=RoutineType.from_text(routine_type_text))
