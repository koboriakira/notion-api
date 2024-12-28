from datetime import date, timedelta
from enum import Enum

from lotion.properties import Select

from common.value.database_type import DatabaseType

kind_map = {
    "月末": {"selected_id": "6e0a84e9-17d8-49ec-8d75-117935f3c4ee", "selected_color": "gray"},
    "毎月1日": {"selected_id": "7bc74ed0-6a2b-44bf-9270-723398498e57", "selected_color": "default"},
    "毎日": {"selected_id": "cf42dbf9-6a9d-4375-ad93-543ba7bc3247", "selected_color": "yellow"},
    "毎週水": {"selected_id": "7139c597-0c50-4252-8418-5fb3426714fc", "selected_color": "blue"},
    "3日後": {"selected_id": "d489a62e-74e6-4dac-86cc-01302c0e898c", "selected_color": "orange"},
    "7日後": {"selected_id": "630165b6-46f6-4d24-8ebd-ccc731ed5862", "selected_color": "pink"},
    "毎週火・金": {"selected_id": "c925b802-b5f1-49c6-b9b7-ad55779e44ed", "selected_color": "purple"},
    "毎週土": {"selected_id": "1d561599-7b3b-44d2-9293-fe5553f5ffed", "selected_color": "green"},
}

MONTHLY_OVERFLOW = 13


class RoutineType(Enum):
    MONTHLY_1 = "毎月1日"
    DAILY = "毎日"
    EVERY_SAT = "毎週土"
    EVERY_TUE_AND_FRI = "毎週火・金"
    EVERY_WED = "毎週水"
    DAYS_AFTER_7 = "7日後"
    DAYS_AFTER_3 = "3日後"
    MONTHLY_END = "月末"

    def next_date(self, basis_date: date) -> date:  # noqa: PLR0911
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
            case RoutineType.MONTHLY_END:
                month = basis_date.month + 1
                if month == MONTHLY_OVERFLOW:
                    return basis_date.replace(year=basis_date.year + 1, month=1, day=1) - timedelta(days=1)
                return basis_date.replace(month=month, day=1) - timedelta(days=1)
            case _:
                msg = f"RoutineType not found: {self}"
                raise ValueError(msg)

    @property
    def selected_name(self) -> str:
        return self.value

    @property
    def selected_id(self) -> str:
        return kind_map[self.value]["selected_id"]

    @property
    def selected_color(self) -> str:
        return kind_map[self.value]["selected_color"]

    @staticmethod
    def from_text(text: str) -> "RoutineType":
        for routine_type in RoutineType:
            if routine_type.value == text:
                return routine_type
        msg = f"RoutineType not found: {text}"
        raise ValueError(msg)


class RoutineKind(Select):
    NAME = "周期"

    def __init__(self, routine_type: RoutineType) -> None:
        super().__init__(
            name=self.NAME,
            selected_name=routine_type.selected_name,
            selected_id=routine_type.selected_id,
            selected_color=routine_type.selected_color,
            id=None,
        )

    @classmethod
    def create(cls, routine_type: RoutineType) -> "RoutineKind":
        return cls(routine_type=routine_type)


if __name__ == "__main__":
    # 最新の情報を取得するときに使う
    # python -m notion_api.task.domain.routine_kind
    from util.localonly import get_select

    get_select(database_id=DatabaseType.TASK_ROUTINE.value, name=RoutineKind.NAME)
