from enum import Enum
from typing import Optional

class ProjectStatus(Enum):
    """
    プロジェクトのステータス
    """
    ICEBOX = "IceBox"
    SUSPEND = "Suspend"
    INBOX = "Inbox"
    NEXT_ACTION = "Next action"
    NOT_STARTED = "Not started"
    IN_PROGRESS = "In progress"
    SCHEDULED = "Scheduled"
    DONE = "Done"
    ARCHIVED = "Archived"
    TRASH = "Trash"
    PRIMARY = "Primary"

    @staticmethod
    def get_status_list(status_str: Optional[str] = None) -> list['ProjectStatus']:
        if status_str is None:
            return [s for s in ProjectStatus]
        if status_str.lower() == "all":
            return [s for s in ProjectStatus]

        str_list = status_str.split(",")
        result: list[ProjectStatus] = []
        for s in str_list:
            try:
                result.append(ProjectStatus(s))
            except ValueError:
                raise Exception("invalid status: " + status_str)
        return result
