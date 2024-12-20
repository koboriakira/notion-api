from enum import Enum

from lotion.properties import Status


class GoalStatusType(Enum):
    INBOX = "Inbox"
    IN_PROGRESS = "In progress"
    SUSPEND = "Suspend"
    TRASH = "Trash"
    DONE = "Done"

    @staticmethod
    def from_text(text: str) -> "GoalStatusType":
        for status_type in GoalStatusType:
            if status_type.value.lower() == text.lower():
                return status_type
        msg = f"GoalStatusType に存在しない値です: {text}"
        raise ValueError(msg)

    @staticmethod
    def get_status_list(status_list: list[str] | None) -> list["GoalStatusType"]:
        if status_list is None:
            return []
        return [GoalStatusType.from_text(status) for status in status_list]

    def is_inbox(self) -> bool:
        return self == GoalStatusType.INBOX

    def is_done(self) -> bool:
        return self == GoalStatusType.DONE

    def is_in_progress(self) -> bool:
        return self == GoalStatusType.IN_PROGRESS


class GoalStatus(Status):
    NAME = "ステータス"

    def __init__(self, status_type: GoalStatusType) -> None:
        super().__init__(self.NAME, status_type.value)

    @staticmethod
    def from_status_type(status_type: GoalStatusType) -> "GoalStatus":
        return GoalStatus(status_type=status_type)
