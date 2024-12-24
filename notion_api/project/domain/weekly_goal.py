from lotion.properties import Text


class WeeklyGoal(Text):
    NAME = "今週の目標"

    @staticmethod
    def from_plain_text(text: str) -> "WeeklyGoal":
        text_model = Text.from_plain_text(name=WeeklyGoal.NAME, text=text)
        return WeeklyGoal(
            name=text_model.name,
            rich_text=text_model.rich_text,
        )
