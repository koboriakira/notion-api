import json
import logging
from typing import Any

from fastapi import APIRouter

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

@router.post("/")
def post(data: Any) -> BaseResponse:
    """
    Return a greeting
    """
    try:
        print("notion_webhook: get")
        logging.debug("notion_webhook: get")
        logging.info("notion_webhook: get")
        print(data)
        print(json.dumps(data, ensure_ascii=False))
        return BaseResponse()
    except Exception as e:
        print(e)
        return BaseResponse(message="Error", data=e)
