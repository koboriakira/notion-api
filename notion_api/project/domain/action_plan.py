from lotion.properties import Text


class ActionPlan(Text):
    NAME = "アクションプラン"

    @classmethod
    def from_plain_text(cls: "ActionPlan", text: str) -> "ActionPlan":
        text_model = Text.from_plain_text(name=cls.NAME, text=text)
        return ActionPlan(
            name=text_model.name,
            rich_text=text_model.rich_text,
        )
