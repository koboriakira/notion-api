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
    def get_status_list(status_list: list[str]) -> list['TaskStatus']:
        if len(status_list) == 0:
            return [s for s in TaskStatus]

        result: list[TaskStatus] = []
        for status_str in status_list:
            for status in TaskStatus:
                if status.value.upper() == status_str.upper():
                    result.append(status)
                    break
        return result
