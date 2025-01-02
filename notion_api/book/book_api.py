from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import date


class NotFoundApiError(Exception):
    def __init__(self, param: str) -> None:
        self.param = param
        super().__init__(f"Not found API result for {param}")


@dataclass(frozen=True)
class BookApiResult:
    title: str
    authors: list[str] | None = None
    publisher: str | None = None
    published_date: date | None = None
    image_url: str | None = None
    url: str | None = None


class BookApiResultConverter:
    @staticmethod
    def of(volume_info: dict) -> BookApiResult:
        image_links: dict | None = volume_info.get("imageLinks")
        return BookApiResult(
            title=volume_info["title"],
            authors=volume_info.get("authors"),
            publisher=volume_info.get("publisher"),
            published_date=BookApiResultConverter._get_published_date(volume_info),
            image_url=image_links.get("medium") if image_links else None,
            url=volume_info.get("infoLink"),
        )

    @staticmethod
    def _get_published_date(volume_info: dict) -> date | None:
        published_date = volume_info.get("publishedDate")
        if published_date is None:
            return None
        try:
            return date.fromisoformat(published_date)
        except ValueError:
            return None


class BookApi(metaclass=ABCMeta):
    @abstractmethod
    def find_by_title(self, title: str) -> BookApiResult:
        """
        Find a book by title

        Args:
            title: Title of the book

        Returns:
            BookApiResult: Book API result

        Raises:
            NotFoundApiError: If the book is not found
        """

    @abstractmethod
    def find_by_id(self, book_id: str) -> BookApiResult:
        """
        Find a book by ID

        Args:
            book_id: ID of the book

        Returns:
            BookApiResult: Book API result

        Raises:
            NotFoundApiError: If the book is not found
        """

    @abstractmethod
    def find_by_isbn(self, isbn: str) -> BookApiResult:
        """
        Find a book by ISBN

        Args:
            isbn: ISBN of the book

        Returns:
            BookApiResult: Book API result

        Raises:
            NotFoundApiError: If the book is not found
        """
