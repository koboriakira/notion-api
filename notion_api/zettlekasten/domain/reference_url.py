from lotion.properties import Url


class ReferenceUrl(Url):
    NAME = "記事"
    def __init__(self, url: str) -> None:
        super().__init__(
            name=self.NAME,
            url=url,
        )
