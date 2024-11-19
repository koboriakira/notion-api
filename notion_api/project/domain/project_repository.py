from abc import ABCMeta, abstractmethod

from project.domain.project import Project


class ProjectRepository(metaclass=ABCMeta):
    @abstractmethod
    def fetch_all(self) -> list[Project]:
        pass

    @abstractmethod
    def archive(self, project: Project) -> None:
        """プロジェクトをバックアップ用にアーカイブする"""

    @abstractmethod
    def remove(self, project: Project) -> None:
        """プロジェクトを削除する"""
