from pydantic import BaseModel

class AddFeelingRequest(BaseModel):
    page_id: str
    value: str
