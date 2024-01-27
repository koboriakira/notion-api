from pydantic import Field
from typing import Optional
from datetime import date as Date
from router.response.base_response import BaseResponse
from router.response.base_notion_page_model import BaseNotionPageModel
from domain.task.task_status import TaskStatus
from custom_logger import get_logger

logger = get_logger(__name__)

class Task(BaseNotionPageModel):
    status: TaskStatus
    task_kind: Optional[str]
    start_date: Optional[Date]
    feeling: Optional[str]

    @staticmethod
    def from_params(params: dict) -> "Task":
        logger.debug(f"params:")
        logger.debug(params)
        return Task(
            id=params["id"],
            url=params["url"],
            title=params["title"],
            created_at=params["created_at"],
            updated_at=params["updated_at"],
            status=TaskStatus(params["status"]),
            task_kind=params.get("task_kind"),
            start_date=params.get("start_date"),
            feeling=params.get("feeling"),
        )

class TaskResponse(BaseResponse):
    data: Optional[Task]

class TasksResponse(BaseResponse):
    data: list[Task] = Field(default=[])
