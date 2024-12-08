from abc import ABCMeta, abstractmethod

from goal.domain.goal import Goal


class GoalRepository(metaclass=ABCMeta):
    @abstractmethod
    def fetch_all(self, include_children: bool | None = None) -> list[Goal]:
        pass

    @abstractmethod
    def remove(self, project: Goal) -> None:
        """目標を削除する"""

    @abstractmethod
    def archive(self, project: Goal) -> None:
        """目標をバックアップ用にアーカイブする"""
