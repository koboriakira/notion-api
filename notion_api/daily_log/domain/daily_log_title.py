from datetime import date

from notion_client_wrapper.properties.title import Title


class DailyLogTitle(Title):
    NAME = "名前"

    def __init__(self, text: str) -> None:
        super().__init__(
            name=self.NAME,
            text=text,
        )

    @classmethod
    def from_date(cls: "DailyLogTitle", date_: date) -> "DailyLogTitle":
        DailyLogTitle(text=date_.isoformat())
