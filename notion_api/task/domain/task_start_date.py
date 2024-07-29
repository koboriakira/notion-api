from datetime import date, datetime

from notion_client_wrapper.properties.date import Date


class TaskStartDate(Date):
    NAME = "実施日"

    def __init__(self, start_date: date | datetime | None) -> None:
        super().__init__(
            name=self.NAME,
            start=start_date.isoformat() if start_date is not None else None,
        )

    @classmethod
    def create(cls, start_date: date | datetime | None) -> "TaskStartDate":
        return TaskStartDate(start_date=start_date)
