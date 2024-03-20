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
    def from_text(text: str) -> "TaskStatusType":
        for status_type in TaskStatusType:
            if status_type.value.lower() == text.lower():
                return status_type
        msg = f"TaskStatusType に存在しない値です: {text}"
        raise ValueError(msg)

    @staticmethod
    def get_status_list(status_list: list[str]|None) -> list["TaskStatusType"]:
        if status_list is None:
            return []
        return [TaskStatusType.from_text(status) for status in status_list]

class TaskStatus(Status):
    NAME = "ステータス"
    def __init__(self, status_type: TaskStatusType) -> None:
        super().__init__(
            self.NAME,
            status_type.value)

    @classmethod
    def from_status_type(cls: "TaskStatus", status_type: TaskStatusType) -> "TaskStatus":
        return cls(status_type=status_type)
