import json
import os

import requests

from domain.slack.slack_concierge_api import SlackConciergeAPI


class LambdaSlackConciergeAPI(SlackConciergeAPI):
    def __init__(self) -> None:
        self.domain = os.getenv("LAMBDA_SLACK_CONCIERGE_API_DOMAIN")

    def append_context_block(self, channel: str, event_ts: str, context: dict) -> None:
        url = f"{self.domain}message/{channel}/{event_ts}/block/add_context"
        data = {
            "data": context,
        }
        self._post(url, data)

    def _post(self, url: str, data: dict) -> None:
        response = requests.post(url, json=data, timeout=30)
        if response.status_code != 200:
            data_str = json.dumps(data, ensure_ascii=False)
            error_messsage = f"Failed to post to {url}. status_code: {response.status_code}, response: {response.text}, data: {data_str}"
            raise Exception(error_messsage)


if __name__ == "__main__":
    # python -m notion_api.infrastructure.slack.lambda_slack_concierge_api
    api = LambdaSlackConciergeAPI()
    api.append_context_block("C05H3USHAJU", "1710342408.079219", {"foo": "bar"})
