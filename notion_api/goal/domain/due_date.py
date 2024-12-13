from datetime import date

from lotion.properties import Date


class DueDate(Date):
    NAME = "期限"

    def __init__(self, date_: date | None) -> None:
        super().__init__(
            name=self.NAME,
            start=date_.isoformat() if date_ is not None else None,
        )

    @classmethod
    def create(cls: "DueDate", date_: date) -> "DueDate":
        return DueDate(date_=date_)

    @classmethod
    def empty(cls: "DueDate") -> "DueDate":
        return DueDate(date_=None)
