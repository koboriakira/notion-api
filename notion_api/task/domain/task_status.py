from enum import Enum


class TaskStatusType(Enum):
    """
    タスクのステータス
    """

    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"

    def is_done(self) -> bool:
        return self == TaskStatusType.DONE

    def is_in_progress(self) -> bool:
        return self == TaskStatusType.IN_PROGRESS

    def is_todo(self) -> bool:
        return self == TaskStatusType.TODO
