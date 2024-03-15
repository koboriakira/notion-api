from datetime import date as Date
from datetime import datetime as Datetime

from pydantic import Field

from custom_logger import get_logger
from domain.task.task_status import TaskStatusType
from router.response.base_notion_page_model import BaseNotionPageModel
from router.response.base_response import BaseResponse
from util.datetime import JST

logger = get_logger(__name__)


def convert_to_datetime(value: str | None) -> Datetime | None:
    if value is None:
        return None
    if len(value) == 10:
        date = Date.fromisoformat(value)
        return Datetime(date.year, date.month, date.day, tzinfo=JST)
    else:
        return Datetime.fromisoformat(value)

class Task(BaseNotionPageModel):
    status: TaskStatusType
    task_kind: str | None
    start_date: Datetime | None
    end_date: Datetime | None
    feeling: str | None

    @staticmethod
    def from_params(params: dict) -> "Task":
        # logger.debug(f"params:")
        return Task(
            id=params["id"],
            url=params["url"],
            title=params["title"],
            created_at=params["created_at"],
            updated_at=params["updated_at"],
            status=TaskStatusType(params["status"]),
            task_kind=params.get("task_kind"),
            start_date=convert_to_datetime(params.get("start_date")),
            end_date=convert_to_datetime(params.get("end_date")),
            feeling=params.get("feeling"),
        )

class TaskResponse(BaseResponse):
    data: Task | None

class TasksResponse(BaseResponse):
    data: list[Task] = Field(default=[])
