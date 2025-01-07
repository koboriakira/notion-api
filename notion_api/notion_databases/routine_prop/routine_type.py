from calendar import FRIDAY
from datetime import date, timedelta
from enum import Enum

MONTHLY_OVERFLOW = 13
FRIDAY = 4


def add_a_month(date: date) -> tuple[int, int]:
    month = date.month + 1
    if month == MONTHLY_OVERFLOW:
        return date.year + 1, 1
    return date.year, month


def get_first_friday(year: int, month: int) -> date:
    for day in range(1, 8):
        date_ = date(year=year, month=month, day=day)
        if date_.weekday() == FRIDAY:
            return date_
    raise ValueError("First Friday not found")


def get_third_friday(year: int, month: int) -> date:
    first_friday = get_first_friday(year, month)
    return first_friday + timedelta(days=14)


class RoutineType(Enum):
    MONTHLY_1 = "毎月1日"
    MONTHLY_25 = "毎月25日"
    DAILY = "毎日"
    EVERY_SAT = "毎週土"
    EVERY_TUE_AND_FRI = "毎週火・金"
    EVERY_WED = "毎週水"
    DAYS_AFTER_7 = "7日後"
    DAYS_AFTER_3 = "3日後"
    DAYS_AFTER_20 = "20日後"
    MONTHLY_END = "月末"
    MONTHLY_1_3_FRI = "第1・3金"

    def next_date(self, basis_date: date) -> date:  # noqa: C901, PLR0911, PLR0912
        """タスクの次回予定日を返す"""
        weekday = basis_date.weekday()
        match self:
            case RoutineType.MONTHLY_1:
                year, month = add_a_month(basis_date)
                return date(year=year, month=month, day=1)
            case RoutineType.MONTHLY_25:
                date_ = basis_date.replace(day=25)
                if basis_date < date_:
                    return date_
                year, month = add_a_month(basis_date)
                return date(year=year, month=month, day=25)
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
            case RoutineType.MONTHLY_1_3_FRI:
                first_friday = get_first_friday(basis_date.year, basis_date.month)
                if basis_date < first_friday:
                    return first_friday
                third_friday = get_third_friday(basis_date.year, basis_date.month)
                if basis_date < third_friday:
                    return third_friday
                year, month = add_a_month(basis_date)
                return get_first_friday(year, month)
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
