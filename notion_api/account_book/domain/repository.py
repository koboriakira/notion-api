from abc import ABCMeta, abstractmethod

from account_book.domain.account_book import AccountBook


class Repository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, entity: AccountBook) -> AccountBook:
        """Save a AccountBook item."""
