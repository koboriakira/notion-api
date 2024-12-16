from lotion.properties import Text


class DailyRetroComment(Text):
    NAME = "ふりかえり"

    @classmethod
    def from_plain_text(cls: "DailyRetroComment", text: str) -> "DailyRetroComment":
        text_model = Text.from_plain_text(name=cls.NAME, text=text)
        return DailyRetroComment(
            name=text_model.name,
            rich_text=text_model.rich_text,
        )
