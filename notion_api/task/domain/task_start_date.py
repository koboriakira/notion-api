from datetime import date, datetime

from lotion.properties import Date


class TaskStartDate(Date):
    NAME = "実施日"

    def __init__(self,
                 start_date: date | datetime | None = None,
                 end_date: date | datetime | None = None,
                 ) -> None:
        super().__init__(
            name=self.NAME,
            start=start_date.isoformat() if start_date is not None else None,
            end=end_date.isoformat() if end_date is not None else None,
        )

    @classmethod
    def create(cls,
               start_date: date | datetime | None = None,
               end_date: date | datetime | None = None,
            ) -> "TaskStartDate":
        if isinstance(start_date, datetime) and start_date.time() == datetime.min.time():
            start_date = start_date.date()
        if isinstance(end_date, datetime) and end_date.time() == datetime.min.time():
            end_date = end_date.date()
        return TaskStartDate(start_date=start_date, end_date=end_date)
