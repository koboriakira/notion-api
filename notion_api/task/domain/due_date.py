from datetime import date, datetime

from lotion.properties import Date


class DueDate(Date):
    NAME = "締め切り"

    def __init__(self, _date: date | datetime | None) -> None:
        super().__init__(
            name=self.NAME,
            start=_date.isoformat() if _date is not None else None,
        )

    @classmethod
    def create(cls, _date: date | datetime | None) -> "DueDate":
        return DueDate(_date=_date)
