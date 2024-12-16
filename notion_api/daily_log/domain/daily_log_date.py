from datetime import date

from lotion.properties import Date


class DailyLogDate(Date):
    NAME = "日付"

    def __init__(self, date_: date | None) -> None:
        super().__init__(
            name=self.NAME,
            start=date_.isoformat() if date_ is not None else None,
        )

    @classmethod
    def create(cls: "DailyLogDate", date_: date) -> "DailyLogDate":
        return DailyLogDate(date_=date_)

    @classmethod
    def empty(cls: "DailyLogDate") -> "DailyLogDate":
        return DailyLogDate(date_=None)
