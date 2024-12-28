from datetime import date, timedelta
from enum import Enum

MONTHLY_OVERFLOW = 13


class RoutineType(Enum):
    MONTHLY_1 = "毎月1日"
    DAILY = "毎日"
    EVERY_SAT = "毎週土"
    EVERY_TUE_AND_FRI = "毎週火・金"
    EVERY_WED = "毎週水"
    DAYS_AFTER_7 = "7日後"
    DAYS_AFTER_3 = "3日後"
    DAYS_AFTER_20 = "20日後"
    MONTHLY_END = "月末"

    def next_date(self, basis_date: date) -> date:  # noqa: C901, PLR0911
        """タスクの次回予定日を返す"""
        weekday = basis_date.weekday()
        match self:
            case RoutineType.MONTHLY_1:
                month = basis_date.month + 1
                if month == MONTHLY_OVERFLOW:
                    return basis_date.replace(year=basis_date.year + 1, month=1, day=1)
                return basis_date.replace(month=month, day=1)
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
            case RoutineType.DAYS_AFTER_20:
                return basis_date + timedelta(days=20)
            case RoutineType.MONTHLY_END:
                month = basis_date.month + 1
                if month == MONTHLY_OVERFLOW:
                    return basis_date.replace(year=basis_date.year + 1, month=1, day=1) - timedelta(days=1)
                return basis_date.replace(month=month, day=1) - timedelta(days=1)
            case _:
                msg = f"RoutineType not found: {self}"
                raise ValueError(msg)

    @staticmethod
    def from_text(text: str) -> "RoutineType":
        for routine_type in RoutineType:
            if routine_type.value == text:
                return routine_type
        msg = f"RoutineType not found: {text}"
        raise ValueError(msg)
