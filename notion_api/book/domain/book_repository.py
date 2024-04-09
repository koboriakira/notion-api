from abc import ABCMeta, abstractmethod

from book.domain.book import Book


class BookRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_title(self, title: str) -> Book | None:
        """Find a book by title"""

    @abstractmethod
    def save(self, book: Book) -> Book:
        """Save a book"""
