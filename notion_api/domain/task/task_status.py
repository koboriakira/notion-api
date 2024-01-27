from enum import Enum
from typing import Optional

class TaskStatus(Enum):
    """
    タスクのステータス
    """
    TODO= "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"

    @staticmethod
    def get_status_list(status_str: Optional[str] = None) -> list['TaskStatus']:
        if status_str is None:
            return [s for s in TaskStatus]
        if status_str.lower() == "all":
            return [s for s in TaskStatus]

        str_list = status_str.split(",")
        result: list[TaskStatus] = []
        for s in str_list:
            try:
                result.append(TaskStatus(s))
            except ValueError:
                raise Exception("invalid status: " + status_str)
        return result
