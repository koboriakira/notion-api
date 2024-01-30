from pydantic import BaseModel
from datetime import date as Date
from datetime import datetime as Datetime
from typing import Optional

class CreateNewTaskRequest(BaseModel):
    title: Optional[str] = None
    mentioned_page_id: Optional[str] = None
    start_date: Optional[Date|Datetime] = None
    end_date: Optional[Date|Datetime] = None
