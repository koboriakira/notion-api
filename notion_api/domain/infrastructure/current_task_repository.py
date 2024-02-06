from abc import ABCMeta, abstractmethod
from typing import Optional

class CurrentTaskRepository(metaclass=ABCMeta):
    """
    今日のタスクを管理するリポジトリ
    """

    @abstractmethod
    def save(self, tasks: list[dict]) -> bool:
        """
        タスク一覧を保存する
        """
        pass

    @abstractmethod
    def load(self) -> list[dict]:
        """
        タスク一覧を取得する
        """
        pass
