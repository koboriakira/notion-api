from datetime import date

from lotion.properties import Title


class DailyLogTitle(Title):
    NAME = "名前"

    def __init__(self, text: str) -> None:
        title = Title.from_plain_text(name=self.NAME, text=text)
        super().__init__(
            name=title.name,
            rich_text=title.rich_text,
        )

    @staticmethod
    def from_date(date_: date) -> "DailyLogTitle":
        return DailyLogTitle(text=date_.isoformat())
