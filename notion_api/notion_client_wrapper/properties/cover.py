from dataclasses import dataclass

from requests import HTTPError

from notion_client_wrapper.unsplash.unsplash_photo import UnsplashPhoto


@dataclass
class Cover:
    type: str
    external_url: str | None = None

    def __init__(self, type: str, external_url: str | None = None) -> None:  # noqa: A002
        self.type = type
        self.external_url = external_url

    @staticmethod
    def of(param: dict) -> "Cover":
        return Cover(
            type=param["type"],
            external_url=param["external"]["url"] if "external" in param else None,
        )

    @staticmethod
    def from_external_url(external_url: str) -> "Cover":
        return Cover(
            type="external",
            external_url=external_url,
        )

    @staticmethod
    def random(query_words: list[str] | None = None) -> "Cover | None":
        query_words = query_words or ["nature"]
        try:
            external_url = UnsplashPhoto().get_random_photo_url(query_words=query_words)
            return Cover.from_external_url(external_url=external_url)
        except HTTPError:
            return None

    def __dict__(self) -> dict:
        result = {
            "type": self.type,
        }
        if self.external_url is not None:
            result["external"] = {
                "url": self.external_url,
            }
        return result

    def value_for_filter(self) -> str:
        raise NotImplementedError
