from dataclasses import dataclass
from datetime import date, datetime, timedelta

from util.dataclass.type_safe_object import TypeSafeFrozenObject


@dataclass(frozen=True)
class Isoweek(TypeSafeFrozenObject):
    year: int
    isoweeknum: int
    start_date: date
    end_date: date

    @staticmethod
    def of(date_: date | datetime) -> "Isoweek":
        assert isinstance(date_, date)
        if isinstance(date_, datetime):
            date_ = date_.date()
        year, isoweeknum, _ = date_.isocalendar()
        start_date = date_.fromisocalendar(year, isoweeknum, 1)
        end_date = date_.fromisocalendar(year, isoweeknum, 7)
        return Isoweek(
            year=year,
            isoweeknum=isoweeknum,
            start_date=start_date,
            end_date=end_date,
        )

    def date_range(self) -> list[date]:
        return [self.start_date + timedelta(days=i) for i in range(7)]

    def __str__(self) -> str:
        return f"{self.year}-Week{self.isoweeknum}"
