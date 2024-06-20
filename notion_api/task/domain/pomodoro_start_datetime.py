from datetime import datetime

from notion_client_wrapper.properties.date import Date


class PomodoroStartDatetime(Date):
    NAME = "ポモドーロ開始"

    def __init__(self, start_date: datetime) -> None:
        super().__init__(
            name=self.NAME,
            start=start_date.isoformat(),
        )
