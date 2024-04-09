from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class BookApiResult:
    title: str
    authors: list[str]
    publisher: str | None
    published_date: date | None
    image_url: str | None
    url: str | None


class BookApiResultConverter:
    @classmethod
    def of(cls: "BookApiResultConverter", volume_info: dict) -> BookApiResult:
        return BookApiResult(
            title=volume_info.get("title"),
            authors=volume_info.get("authors"),
            publisher=volume_info.get("publisher"),
            published_date=cls.__get_published_date(volume_info),
            image_url=volume_info.get("imageLinks").get("medium"),
            url=volume_info.get("infoLink"),
        )

    @staticmethod
    def __get_published_date(volume_info: dict) -> date | None:
        published_date = volume_info.get("publishedDate")
        if published_date is None:
            return None
        try:
            return date.fromisoformat(published_date)
        except ValueError:
            return None


class BookApi(metaclass=ABCMeta):
    @abstractmethod
    def find_by_title(self, title: str) -> BookApiResult | None:
        pass

    @abstractmethod
    def find_by_id(self, book_id: str) -> BookApiResult:
        pass

    @abstractmethod
    def find_by_isbn(self, isbn: str) -> BookApiResult | None:
        pass
