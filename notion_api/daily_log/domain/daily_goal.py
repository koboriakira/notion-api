from lotion.properties import Text


class DailyGoal(Text):
    NAME = "目標"

    @staticmethod
    def from_plain_text(text: str) -> "DailyGoal":
        text_model = Text.from_plain_text(name=DailyGoal.NAME, text=text)
        return DailyGoal(
            name=text_model.name,
            rich_text=text_model.rich_text,
        )
