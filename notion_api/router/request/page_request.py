from pydantic import BaseModel


class AddFeelingRequest(BaseModel):
    page_id: str
    value: str


class AddPomodoroCountRequest(BaseModel):
    page_id: str
    count: int | None


class UpdateStatusRequest(BaseModel):
    page_id: str
    value: str


class AppendTextBlockRequest(BaseModel):
    page_id: str
    value: str


class AppendImageBlockRequest(BaseModel):
    image_url: str
