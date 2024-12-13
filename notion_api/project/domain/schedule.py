from datetime import date, datetime

from lotion.properties import Date


class Schedule(Date):
    NAME = "開始可能日"

    def __init__(self, start_date: date | datetime | None, end_date: date | datetime | None) -> None:
        super().__init__(
            name=self.NAME,
            start=start_date.isoformat() if start_date is not None else None,
            end=end_date.isoformat() if end_date is not None else None,
        )

    @classmethod
    def create(
        cls: "Schedule",
        start_date: date | datetime | None = None,
        end_date: date | datetime | None = None,
    ) -> "Schedule":
        return Schedule(start_date=start_date, end_date=end_date)
