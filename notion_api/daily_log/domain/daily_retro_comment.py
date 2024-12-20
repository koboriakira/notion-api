from lotion.properties import Text


class DailyRetroComment(Text):
    NAME = "ふりかえり"

    @staticmethod
    def from_plain_text(text: str) -> "DailyRetroComment":
        text_model = Text.from_plain_text(name=DailyRetroComment.NAME, text=text)
        return DailyRetroComment(
            name=text_model.name,
            rich_text=text_model.rich_text,
        )
