
from notion_client_wrapper.block.rich_text import RichText
from notion_client_wrapper.properties.text import Text


class Publisher(Text):
    NAME = "出版社"

    def __init__(self, name: str, rich_text: RichText) -> None:
        super().__init__(
            name=name,
            rich_text=rich_text,
        )

    @classmethod
    def create(cls: "Publisher", text: str) -> "Publisher":
        text_property = Text.from_plain_text(name=cls.NAME, text=text)
        return Publisher(
            name=text_property.name,
            rich_text=text_property.rich_text)
