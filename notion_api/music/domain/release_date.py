from datetime import date

from notion_client_wrapper.properties.date import Date


class ReleaseDate(Date):
    NAME = "リリース日"

    def __init__(self, date_: date) -> None:
        super().__init__(
            name=self.NAME,
            start=date_.isoformat(),
        )
