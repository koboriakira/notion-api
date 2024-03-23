from datetime import date, datetime

from pydantic import Field

from custom_logger import get_logger
from domain.task.task import Task as TaskModel
from domain.task.task_status import TaskStatusType
from router.response.base_notion_page_model import BaseNotionPageModel
from router.response.base_response import BaseResponse
from util.datetime import convert_to_date_or_datetime

logger = get_logger(__name__)



class Task(BaseNotionPageModel):
    status: TaskStatusType
    task_kind: str | None # FIXME: TaskKindTypeにする
    start_date: datetime| date | None
    end_date: datetime| date | None # FIXME: 消す
    feeling: str | None # FIXME: 消す

    @staticmethod
    def from_params(params: dict) -> "Task":
        return Task(
            id=params["id"],
            url=params["url"],
            title=params["title"],
            created_at=params["created_at"],
            updated_at=params["updated_at"],
            status=TaskStatusType(params["status"]),
            task_kind=params.get("task_kind"),
            start_date=convert_to_date_or_datetime(params.get("start_date")),
            end_date=convert_to_date_or_datetime(params.get("end_date")),
            feeling=params.get("feeling"),
            text=params.get("text"),
        )

class TaskResponse(BaseResponse):
    data: Task | None

    @staticmethod
    def from_model(model: TaskModel) -> "TaskResponse":
        task = Task(
            id=model.id,
            url=model.url,
            title=model.get_title_text(),
            created_at=model.created_time.start_time,
            updated_at=model.last_edited_time.start_time,
            status=model.status,
            task_kind=model.kind.value,
            start_date=model.start_datetime,
            end_date=None,
            feeling="",
            text="",
        )
        return TaskResponse(data=task)

class TasksResponse(BaseResponse):
    data: list[Task] = Field(default=[])
