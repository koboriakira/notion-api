from datetime import date

from notion_client_wrapper.properties.date import Date


class PublishedDate(Date):
    NAME = "出版日"

    def __init__(self, name: str, start_date: date) -> None:
        super().__init__(
            name=name,
            start=start_date.isoformat(),
        )

    @classmethod
    def create(cls: "PublishedDate", start_date: date) -> "PublishedDate":
        return PublishedDate(name=cls.NAME, start_date=start_date)
