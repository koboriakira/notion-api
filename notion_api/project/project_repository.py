from abc import ABCMeta, abstractmethod

from notion_databases.project import Project


class ProjectRepository(metaclass=ABCMeta):
    @abstractmethod
    def fetch_all(self) -> list[Project]:
        pass

    @abstractmethod
    def archive(self, project: Project) -> None:
        """プロジェクトをバックアップ用にアーカイブする"""

    @abstractmethod
    def save(self, project: Project) -> Project:
        """プロジェクトを保存する"""

    @abstractmethod
    def find_by_id(self, page_id: str) -> Project:
        """プロジェクトを取得する"""

    @abstractmethod
    def remove(self, project: Project) -> None:
        """プロジェクトを削除する"""
