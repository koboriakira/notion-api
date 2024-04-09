from notion_client_wrapper.properties.title import Title


class BookTitle(Title):
    NAME = "Title"

    def __init__(self, text: str) -> None:
        super().__init__(
            name=self.NAME,
            text=text,
        )
