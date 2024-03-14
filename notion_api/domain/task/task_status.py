from enum import Enum


class TaskStatus(Enum):
    """
    タスクのステータス
    """
    TODO= "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"

    @staticmethod
    def get_status_list(status_list: list[str]|None) -> list["TaskStatus"]:
        if status_list is not None or len(status_list) == 0:
            return list(TaskStatus)

        result: list[TaskStatus] = []
        for status_str in status_list:
            for status in TaskStatus:
                if status.value.upper() == status_str.upper():
                    result.append(status)
                    break
        return result
