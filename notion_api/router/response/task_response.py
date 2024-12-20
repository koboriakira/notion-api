from datetime import date, datetime

from pydantic import Field

from custom_logger import get_logger
from router.response.base_notion_page_model import BaseNotionPageModel
from router.response.base_response import BaseResponse
from task.domain.task import ToDoTask as TaskModel
from task.domain.task_status import TaskStatusType

logger = get_logger(__name__)


def convert_to_date_if_zero_time(value: datetime | date | None) -> datetime | date | None:
    """時間が0時の場合は日付のみを返す"""
    if value is None:
        return None
    if isinstance(value, datetime) and value.time() == datetime.min.time():
        return value.date()
    return value


class Task(BaseNotionPageModel):
    status: TaskStatusType
    task_kind: str | None  # FIXME: TaskKindTypeにする
    start_date: datetime | date | None
    pomodoro_count: int
    pomodoro_start_datetime: datetime | None
    end_date: datetime | date | None  # FIXME: 消す
    due_date: datetime | date | None
    order: int
    feeling: str | None  # FIXME: 消す

    @staticmethod
    def from_model(model: TaskModel) -> "Task":
        return Task(
            id=model.id,
            url=model.url,
            title=model.get_title_text(),
            created_at=model.created_time,
            updated_at=model.last_edited_time,
            status=model.status,
            pomodoro_count=model.pomodoro_count,
            pomodoro_start_datetime=model.pomodoro_start_datetime,
            task_kind=model.kind.value if model.kind is not None else None,
            start_date=convert_to_date_if_zero_time(model.start_date),
            end_date=None,
            due_date=convert_to_date_if_zero_time(model.due_date),
            order=model.order,
            feeling="",
            text=model.get_slack_text_in_block_children(),
        )


class TaskResponse(BaseResponse):
    data: Task | None


class TasksResponse(BaseResponse):
    data: list[Task] = Field(default=[])
