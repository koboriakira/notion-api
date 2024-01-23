from fastapi import APIRouter, Header
import logging
from router.response import BaseResponse

router = APIRouter()


@router.get("", response_model=BaseResponse)
def healthcheck():
    """
    Return a greeting
    """
    logging.debug("healthcheck")
    logging.info("healthcheck")
    return BaseResponse(message="Healthcheck OK")
