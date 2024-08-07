from abc import ABCMeta, abstractmethod

from shopping.domain.shopping import Shopping


class ShoppingRepository(metaclass=ABCMeta):
    @abstractmethod
    def fetch_all(self) -> list[Shopping]:
        """Fetch all Shopping items."""

    @abstractmethod
    def save(self, song: Shopping) -> Shopping:
        """Save a Shopping item."""
