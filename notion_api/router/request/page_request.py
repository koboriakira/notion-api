from pydantic import BaseModel
from typing import Optional

class AddFeelingRequest(BaseModel):
    page_id: str
    value: str

class AddPomodoroCountRequest(BaseModel):
    page_id: str
    count: Optional[int]

class UpdateStatusRequest(BaseModel):
    page_id: str
    value: str
