from lotion.properties import Url


class SpotifyUrl(Url):
    NAME = "Spotify"

    def __init__(self, url: str) -> None:
        super().__init__(
            name=self.NAME,
            url=url,
        )
