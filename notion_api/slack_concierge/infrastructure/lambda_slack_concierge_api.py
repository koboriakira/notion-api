import json
import os

import requests


class SlackConciergeAPIError(Exception):
    pass

class LambdaSlackConciergeAPI:
    def __init__(self) -> None:
        domain = os.getenv("LAMBDA_SLACK_CONCIERGE_API_DOMAIN")
        if domain is None:
            msg = "LAMBDA_SLACK_CONCIERGE_API_DOMAIN is not set"
            raise SlackConciergeAPIError(msg)
        self._domain = domain

    def append_context_block(self, channel: str, event_ts: str, context: dict) -> None:
        url = f"{self._domain}message/{channel}/{event_ts}/block/add_context"
        data = {
            "data": context,
        }
        self._post(url, data)

    def _post(self, url: str, data: dict) -> None:
        response = requests.post(url, json=data, timeout=30)
        if response.status_code != 200:
            data_str = json.dumps(data, ensure_ascii=False)
            error_messsage = f"Failed to post to {url}. status_code: {response.status_code}, response: {response.text}, data: {data_str}"
            raise SlackConciergeAPIError(error_messsage)
