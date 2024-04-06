from datetime import date, datetime

from pydantic import Field

from custom_logger import get_logger
from router.response.base_notion_page_model import BaseNotionPageModel
from router.response.base_response import BaseResponse
from task.domain.task import Task as TaskModel
from task.domain.task_status import TaskStatusType

logger = get_logger(__name__)


class Task(BaseNotionPageModel):
    status: TaskStatusType
    task_kind: str | None  # FIXME: TaskKindTypeにする
    start_date: datetime | date | None
    pomodoro_count: int
    end_date: datetime | date | None  # FIXME: 消す
    feeling: str | None  # FIXME: 消す

    @staticmethod
    def from_model(model: TaskModel) -> "Task":
        return Task(
            id=model.id,
            url=model.url,
            title=model.get_title_text(),
            created_at=model.created_time.start_time,
            updated_at=model.last_edited_time.start_time,
            status=model.status,
            pomodoro_count=model.pomodoro_count,
            task_kind=model.kind.value if model.kind is not None else None,
            start_date=model.start_datetime if model.start_datetime is not None else None,
            end_date=None,
            feeling="",
            text=model.get_slack_text_in_block_children(),
        )


class TaskResponse(BaseResponse):
    data: Task | None


class TasksResponse(BaseResponse):
    data: list[Task] = Field(default=[])
