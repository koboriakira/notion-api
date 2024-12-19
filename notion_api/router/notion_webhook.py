import json
import logging

from fastapi import APIRouter
from lotion import BasePage
from pydantic import BaseModel

from router.response import BaseResponse

router = APIRouter()


@router.get("/")
def get() -> BaseResponse:
    """
    Return a greeting
    """
    try:
        print("notion_webhook: get")
        logging.debug("notion_webhook: get")
        logging.info("notion_webhook: get")
        return BaseResponse()
    except Exception as e:
        print(e)
        return BaseResponse(message="Error", data=e)


class NotionWebhookRequest(BaseModel):
    source: dict
    data: dict


@router.post("/")
def post(request: NotionWebhookRequest) -> BaseResponse:
    """
    Return a greeting
    """
    try:
        print("notion_webhook: post")
        logging.debug("notion_webhook: post")
        logging.info("notion_webhook: post")
        print(request)
        print(request.data)
        print(json.dumps(request.data, ensure_ascii=False))
        base_page = BasePage.from_data(request.data)
        print(base_page.page_id.value)
        return BaseResponse()
    except Exception as e:
        print(e)
        return BaseResponse(message="Error", data=e)
