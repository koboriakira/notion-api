from abc import ABCMeta, abstractmethod
from datetime import date

from domain.book.book import Book


class BookApiResultConverter:
    @staticmethod
    def convert_to_book_params(volume_info: dict) -> Book:
        title = volume_info.get("title")
        authors = volume_info.get("authors")
        publisher = volume_info.get("publisher")
        published_date = BookApiResultConverter.__get_published_date(volume_info)
        image_url = volume_info.get("imageLinks").get("medium")
        url = volume_info.get("infoLink")

        return Book.create(
            title=title,
            authors=authors,
            publisher=publisher,
            published_date=published_date,
            image_url=image_url,
            url=url,
        )

    @staticmethod
    def __get_published_date(volume_info: dict) -> date|None:
        published_date = volume_info.get("publishedDate")
        if published_date is None:
            return None
        try:
            return date.fromisoformat(published_date)
        except ValueError:
            return None

class BookApi(metaclass=ABCMeta):
    @abstractmethod
    def find_by_title(self, title: str) -> Book|None:
        pass

    @abstractmethod
    def find_by_id(self, book_id: str) -> Book:
        pass

    @abstractmethod
    def find_by_isbn(self, isbn: str) -> Book|None:
        pass
