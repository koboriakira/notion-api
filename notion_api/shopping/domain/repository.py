from abc import ABCMeta, abstractmethod

from shopping.domain.shopping import Shopping


class ShoppingRepository(metaclass=ABCMeta):
    @abstractmethod
    def fetch_all(self) -> list[Shopping]:
        """Fetch all Shopping items."""

    @abstractmethod
    def save(self, entity: Shopping) -> Shopping:
        """Save a Shopping item."""
