from abc import ABCMeta, abstractmethod

from goal.domain.goal import Goal


class GoalRepository(metaclass=ABCMeta):
    @abstractmethod
    def fetch_all(self) -> list[Goal]:
        pass
