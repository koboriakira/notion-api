from lotion.properties import Title


class BookTitle(Title):
    NAME = "名前"

    def __init__(self, text: str) -> None:
        title = Title.from_plain_text(name=self.NAME, text=text)
        super().__init__(
            name=title.name,
            rich_text=title.rich_text,
        )
