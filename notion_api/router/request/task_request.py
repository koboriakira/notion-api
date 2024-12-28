from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel


class Status(str, Enum):
    ToDo = "ToDo"
    InProgress = "InProgress"
    Done = "Done"


class CreateNewTaskRequest(BaseModel):
    task_id: str | None = None
    title: str | None = None
    mentioned_page_id: str | None = None
    start_date: date | datetime | None = None
    end_date: date | datetime | None = None
    status: Status | None = Status.ToDo
    url: str | None = None
    task_kind: str | None = None


class UpdateTaskRequest(BaseModel):
    pomodoro_count: int  # FIXME: 消す
    status: str | None = None
