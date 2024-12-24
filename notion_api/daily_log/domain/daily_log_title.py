from datetime import date

from lotion.properties import Title


class DailyLogTitle(Title):
    NAME = "名前"

    def __init__(self, text: str) -> None:
        super().__init__(
            name=self.NAME,
            text=text,
        )

    @staticmethod
    def from_date(date_: date) -> "DailyLogTitle":
        return DailyLogTitle(text=date_.isoformat())
