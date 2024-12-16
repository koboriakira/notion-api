from datetime import date

from lotion.properties import Date


class ReleaseDate(Date):
    NAME = "リリース日"

    def __init__(self, date_: date) -> None:
        super().__init__(
            name=self.NAME,
            start=date_.isoformat(),
        )
