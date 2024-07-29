from dataclasses import dataclass
from datetime import datetime


@dataclass
class DatePoint:
    value: datetime
    included_point: bool


@dataclass
class DateRange:
    start: DatePoint
    end: DatePoint

    @staticmethod
    def from_datetime(start: datetime, end: datetime) -> "DateRange":
        return DateRange(
            start=DatePoint(value=start, included_point=True),
            end=DatePoint(value=end, included_point=False),
        )
