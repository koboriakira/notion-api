from notion_client_wrapper.properties.text import Text


class Artist(Text):
    NAME = "Artist"

    @classmethod
    def from_plain_text(cls: "Artist", text: str) -> "Artist":
        text_model = Text.from_plain_text(name=cls.NAME, text=text)
        return Artist(
            name=text_model.name,
            rich_text=text_model.rich_text,
        )
