from datetime import date, datetime

from lotion.properties import Date


class ReleaseDate(Date):
    NAME = "リリース日"

    def __init__(self, date_: date | datetime | None) -> None:
        super().__init__(
            name=self.NAME,
            start=date_.isoformat() if date_ is not None else None,
        )
