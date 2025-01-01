from lotion import Lotion

from notion_databases.task import Task


class TaskUtilService:
    def __init__(self, lotion: Lotion | None = None) -> None:
        self._lotion = lotion or Lotion.get_instance()

    def start(self, page_id: str) -> None:
        """
        Start the task.
        """
        task = self._lotion.retrieve_page(page_id, Task)
        self._lotion.update(task.start())

    def postpone(self, page_id: str, days: int) -> None:
        """
        Postpone the task.
        """
        task = self._lotion.retrieve_page(page_id, Task)
        self._lotion.update(task.do_tomorrow())

    def complete(self, page_id: str) -> None:
        """
        Complete the task.
        """
        task = self._lotion.retrieve_page(page_id, Task)
        self._lotion.update(task.complete())
