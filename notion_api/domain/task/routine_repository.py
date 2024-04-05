from abc import ABCMeta, abstractmethod

from domain.task.routine_task import RoutineTask


class RoutineRepository(metaclass=ABCMeta):
    @abstractmethod
    def fetch_all(self) -> list[RoutineTask]:
        pass
