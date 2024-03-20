from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum

from util.datetime import jst_today


class RoutineType(Enum):
    DAILY = "毎日"
    EVERY_SAT = "毎週土"
    EVERY_TUE_AND_FRI = "毎週火・金"
    EVERY_WED = "毎週水"
    DAYS_AFTER_7 = "7日後"
    DAYS_AFTER_3 = "3日後"


    def next_date(self, basis_date: date) -> date:  # noqa: PLR0911
        weekday = basis_date.weekday()
        match self:
            case RoutineType.DAILY:
                return basis_date
            case RoutineType.EVERY_SAT:
                return basis_date + timedelta(days=(5 - weekday) % 7)
            case RoutineType.EVERY_TUE_AND_FRI:
                if weekday in [1, 4]:
                    return basis_date
                if weekday in [2, 3]:
                    return basis_date + timedelta(days=(4 - weekday) % 7)
                return basis_date + timedelta(days=(1 - weekday) % 7)
            case RoutineType.EVERY_WED:
                return basis_date + timedelta(days=(2 - weekday) % 7)
            case RoutineType.DAYS_AFTER_7:
                return basis_date + timedelta(days=7)
            case RoutineType.DAYS_AFTER_3:
                return basis_date + timedelta(days=3)
            case _:
                raise ValueError(f"RoutineType not found: {self}")

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

    def needs_today(self) -> bool:
        today = jst_today()
        next_date = self.routine_type.next_date()
