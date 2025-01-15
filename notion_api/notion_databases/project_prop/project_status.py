from enum import Enum

from lotion import notion_prop
from lotion.properties import Status


class ProjectStatusType(Enum):
    INBOX = "Inbox"
    IN_PROGRESS = "In progress"
    ICEBOX = "Icebox"
    SUSPEND = "Suspend"
    TRASH = "Trash"
    DONE = "Done"

    def is_done(self) -> bool:
        return self == ProjectStatusType.DONE

    def is_in_progress(self) -> bool:
        return self == ProjectStatusType.IN_PROGRESS

    def is_trash(self) -> bool:
        return self == ProjectStatusType.TRASH

    def is_inbox(self) -> bool:
        return self == ProjectStatusType.INBOX

    def is_suspend(self) -> bool:
        return self == ProjectStatusType.SUSPEND


@notion_prop("ステータス")
class ProjectStatus(Status):
    @staticmethod
    def from_status_type(status_type: ProjectStatusType) -> "ProjectStatus":
        return ProjectStatus.from_status_name(status_type.value)
