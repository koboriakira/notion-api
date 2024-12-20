from datetime import date

from lotion.properties import Date


class PublishedDate(Date):
    NAME = "出版日"

    def __init__(self, name: str, date_: date) -> None:
        super().__init__(
            name=name,
            start=date_.isoformat(),
        )

    @staticmethod
    def create(date_: date) -> "PublishedDate":
        return PublishedDate(name=PublishedDate.NAME, date_=date_)
