from pydantic import BaseModel
from datetime import date as Date
from typing import Optional

class CreateNewTaskRequest(BaseModel):
    title: Optional[str] = None
    mentioned_page_id: Optional[str] = None
    start_date: Optional[Date] = None
