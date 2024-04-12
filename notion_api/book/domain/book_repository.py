from abc import ABCMeta, abstractmethod

from book.domain.book import Book


class ExistedBookError(Exception):
    """既に書籍ページが存在するエラー"""

    def __init__(self, title: str) -> None:
        self.title = title
        super().__init__(f"Existed book page for {title}")


class NotFoundBookError(Exception):
    """書籍ページが存在しないエラー"""

    def __init__(self, title: str) -> None:
        self.title = title
        super().__init__(f"Not found book page for {title}")


class BookRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_title(self, title: str) -> Book | None:
        """Find a book by title"""

    @abstractmethod
    def save(self, book: Book) -> Book:
        """Save a book"""
