from notion_client_wrapper.block.rich_text import RichText
from notion_client_wrapper.properties.text import Text


class Overview(Text):
    NAME = "概要"
    def __init__(self, text: str|None = None) -> None:
        super().__init__(
            name=self.NAME,
            rich_text=RichText.from_plain_text(text=text or ""),
        )
