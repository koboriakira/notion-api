from enum import Enum

from notion_client_wrapper.properties.status import Status


class ProjectStatusType(Enum):
    INBOX = "Inbox"
    IN_PROGRESS = "In progress"
    SUSPEND = "Suspend"
    TRASH = "Trash"
    DONE = "Done"

    @staticmethod
    def from_text(text: str) -> "ProjectStatusType":
        for status_type in ProjectStatusType:
            if status_type.value.lower() == text.lower():
                return status_type
        msg = f"ProjectStatusType に存在しない値です: {text}"
        raise ValueError(msg)

    @staticmethod
    def get_status_list(status_list: list[str] | None) -> list["ProjectStatusType"]:
        if status_list is None:
            return []
        return [ProjectStatusType.from_text(status) for status in status_list]

    def is_done(self) -> bool:
        return self == ProjectStatusType.DONE

    def is_in_progress(self) -> bool:
        return self == ProjectStatusType.IN_PROGRESS

    def is_todo(self) -> bool:
        return self == ProjectStatusType.TODO


class ProjectStatus(Status):
    NAME = "ステータス"

    def __init__(self, status_type: ProjectStatusType) -> None:
        super().__init__(self.NAME, status_type.value)

    @classmethod
    def from_status_type(cls: "ProjectStatus", status_type: ProjectStatusType) -> "ProjectStatus":
        return cls(status_type=status_type)
