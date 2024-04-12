from notion_client_wrapper.properties.url import Url


class ReferenceUrl(Url):
    NAME = "Reference"

    def __init__(self, url: str) -> None:
        super().__init__(
            name=self.NAME,
            url=url,
        )
