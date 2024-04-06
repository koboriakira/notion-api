from notion_client_wrapper.properties.url import Url


class SpotifyUrl(Url):
    NAME = "Spotify"

    def __init__(self, url: str) -> None:
        super().__init__(
            name=self.NAME,
            url=url,
        )
