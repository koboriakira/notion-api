from datetime import date, datetime

from pydantic import BaseModel


class CreateNewTaskRequest(BaseModel):
    task_id: str | None = None
    title: str | None = None
    mentioned_page_id: str | None = None
    start_date: date | datetime | None = None
    end_date: date | datetime | None = None
    status: str | None = None
    url: str | None = None
    task_kind: str | None = None

class UpdateTaskRequest(BaseModel):
    pomodoro_count: int
    status: str | None = None
