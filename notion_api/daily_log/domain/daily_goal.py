from notion_client_wrapper.properties.text import Text


class DailyGoal(Text):
    NAME = "目標"

    @classmethod
    def from_plain_text(cls: "DailyGoal", text: str) -> "DailyGoal":
        text_model = Text.from_plain_text(name=cls.NAME, text=text)
        return DailyGoal(
            name=text_model.name,
            rich_text=text_model.rich_text,
        )
