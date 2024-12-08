from abc import ABCMeta, abstractmethod

from food.domain.food import Food


class FoodRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_title(self, title: str) -> Food | None:
        """Find food by title"""

    @abstractmethod
    def save(self, food: Food) -> Food:
        """飲食を保存する"""
