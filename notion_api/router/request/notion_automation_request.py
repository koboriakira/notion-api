# 上記のリクエストを受け取るためのクラスを作成

from pydantic import BaseModel


class NotionAutomationSourceRequest(BaseModel):
    type: str
    automation_id: str
    action_id: str
    event_it: str
    attempt: int


class NotionAutomationDataRequest(BaseModel):
    object: str
    id: str  # object=pageのとき、ボタンが押されたページのID
    properties: dict | None = None


class NotionAutomationRequest(BaseModel):
    # source: NotionAutomationSourceRequest
    data: NotionAutomationDataRequest
