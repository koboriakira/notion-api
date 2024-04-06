from notion_client_wrapper.properties.text import Text


class DefinitionOfDone(Text):
    NAME = "ゴール"

    @classmethod
    def from_plain_text(cls: "DefinitionOfDone", text: str) -> "DefinitionOfDone":
        text_model = Text.from_plain_text(name=cls.NAME, text=text)
        return DefinitionOfDone(
            name=text_model.name,
            rich_text=text_model.rich_text,
        )
