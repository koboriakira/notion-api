import json
import os

import boto3

from custom_logger import get_logger

AWS_ACCOUNT_ID = os.environ.get("AWS_ACCOUNT_ID")
CREATE_PAGE_QUEUE_URL = (
    f"https://sqs.ap-northeast-1.amazonaws.com/{AWS_ACCOUNT_ID}/NotionApi-createPageQueue162E3EBC-P2yQXsUSJdus"
)

logger = get_logger(__name__)

sqs_client = boto3.client("sqs", region_name="ap-northeast-1")


def create_page(
    mode: str,
    params: dict,
) -> dict:
    _send(
        CREATE_PAGE_QUEUE_URL,
        {
            "mode": mode,
            "params": params,
        },
    )


def _send(queue_url: str, message: dict) -> dict:
    sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message if isinstance(message, str) else json.dumps(message),
    )
