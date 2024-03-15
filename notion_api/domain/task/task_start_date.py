from datetime import date

from notion_client_wrapper.properties.date import Date


class TaskStartDate(Date):
    def __init__(self, name: str, start_date: date) -> None:
        super().__init__(
            name=name,
            start=start_date.isoformat(),
        )

    @staticmethod
    def create(start_date: date) -> "TaskStartDate":
        return TaskStartDate(name="実施日", start_date=start_date)
