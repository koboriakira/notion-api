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
