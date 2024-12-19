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
    print("notion_webhook: get")
    logging.debug("notion_webhook: get")
    logging.info("notion_webhook: get")
    return BaseResponse(message="Healthcheck OK")


@router.post("/")
def post(data: Any) -> BaseResponse:
    """
    Return a greeting
    """
    print("notion_webhook: get")
    logging.debug("notion_webhook: get")
    logging.info("notion_webhook: get")
    print(data)
    print(json.dumps(data, ensure_ascii=False))
    return BaseResponse(message="Healthcheck OK")
