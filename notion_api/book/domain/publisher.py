from lotion.block.rich_text import RichText
from lotion.properties import Text


class Publisher(Text):
    NAME = "出版社"

    def __init__(self, name: str, rich_text: RichText) -> None:
        super().__init__(
            name=name,
            rich_text=rich_text,
        )

    @staticmethod
    def create(text: str) -> "Publisher":
        text_property = Text.from_plain_text(name=Publisher.NAME, text=text)
        return Publisher(name=text_property.name, rich_text=text_property.rich_text)
