from datetime import datetime as DateTime
from pydantic import BaseModel, Field
from typing import Any
from router.response.base_response import BaseResponse

class BaseNotionPageModel(BaseModel):
    id: str
    url: str
    title: str
    created_at: DateTime
    updated_at: DateTime
