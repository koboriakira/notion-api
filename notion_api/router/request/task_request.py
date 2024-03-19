from datetime import date as Date
from datetime import datetime as Datetime

from pydantic import BaseModel


class CreateNewTaskRequest(BaseModel):
    task_id: str | None = None
    title: str | None = None
    mentioned_page_id: str | None = None
    start_date: Date | Datetime | None = None
    end_date: Date | Datetime | None = None
    status: str | None = None
    url: str | None = None
