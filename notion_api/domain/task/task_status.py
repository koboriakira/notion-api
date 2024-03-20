from enum import Enum

from notion_client_wrapper.properties.status import Status


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

class TaskStatus(Status):
    NAME = "ステータス"
    def __init__(self, status_type: TaskStatusType) -> None:
        super().__init__(
            self.NAME,
            status_type.value)

    @classmethod
    def from_status_type(cls: "TaskStatus", status_type: TaskStatusType) -> "TaskStatus":
        return cls(status_type=status_type)
