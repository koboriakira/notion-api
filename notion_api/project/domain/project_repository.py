from abc import ABCMeta, abstractmethod

from project.domain.project import Project


class ProjectRepository(metaclass=ABCMeta):
    @abstractmethod
    def fetch_all(self) -> list[Project]:
        pass
