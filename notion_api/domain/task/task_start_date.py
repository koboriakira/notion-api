from datetime import date, datetime

from notion_client_wrapper.properties.date import Date


class TaskStartDate(Date):
    NAME = "実施日"
    def __init__(self, start_date: date|datetime) -> None:
        super().__init__(
            name=self.NAME,
            start=start_date.isoformat(),
        )

    @classmethod
    def create(cls:"TaskStartDate", start_date: date|datetime) -> "TaskStartDate":
        return TaskStartDate(start_date=start_date)
