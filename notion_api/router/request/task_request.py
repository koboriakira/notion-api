from pydantic import BaseModel
from datetime import date as Date
from typing import Optional

class CreateNewTaskRequest(BaseModel):
    title: str
    start_date: Optional[Date] = None
