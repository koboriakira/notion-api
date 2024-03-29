from notion_client_wrapper.properties.title import Title


class ZettlekastenName(Title):
    NAME = "名前"
    def __init__(self, text: str) -> None:
        super().__init__(
            name=self.NAME,
            text=text,
        )
