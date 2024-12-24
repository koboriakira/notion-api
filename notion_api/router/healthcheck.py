import logging

from fastapi import APIRouter

from router.response import BaseResponse
from util.dynamodb.dynamodb import DynamoDBClient

router = APIRouter()


@router.get("")
def healthcheck() -> BaseResponse:
    """
    Return a greeting
    """
    logging.debug("healthcheck")
    logging.info("healthcheck")
    errors = []
    try:
        dynamo_db = DynamoDBClient.get_attributes_client()
        dynamo_db.find("key", "1")
    except Exception as e:  # noqa: BLE001
        errors.append(str(e))
    if errors:
        return BaseResponse(message="Healthcheck failed", data=errors)
    return BaseResponse(message="Healthcheck OK")
