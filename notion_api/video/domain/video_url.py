from lotion.properties import Url


class VideoUrl(Url):
    NAME = "URL"
    def __init__(self, url: str) -> None:
        super().__init__(
            name=self.NAME,
            url=url,
        )
