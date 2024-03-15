from enum import Enum


class TaskStatusType(Enum):
    """
    タスクのステータス
    """
    TODO= "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"

    @staticmethod
    def get_status_list(status_list: list[str]|None) -> list["TaskStatusType"]:
        if status_list is not None or len(status_list) == 0:
            return list(TaskStatusType)

        result: list[TaskStatusType] = []
        for status_str in status_list:
            for status in TaskStatusType:
                if status.value.upper() == status_str.upper():
                    result.append(status)
                    break
        return result
