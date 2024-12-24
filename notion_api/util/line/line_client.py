import json
import os

import requests


class LineClient:
    MESSAGE_PUSH_API = "https://api.line.me/v2/bot/message/push"

    def __init__(self, channel_access_token: str, talk_id: str) -> None:
        self.channel_access_token = channel_access_token
        self.talk_id = talk_id

    @staticmethod
    def get_instance() -> "LineClient":
        channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
        talk_id = os.environ["LINE_TALK_ID"]
        return LineClient(channel_access_token, talk_id)

    def push_message(self, text: str) -> dict:
        return self._post_message(message={"type": "text", "text": text})

    def push_confirm_template(self, template: dict, alt_text: str = "確認メッセージ") -> None:
        self._post_message(message={"type": "template", "altText": alt_text, "template": template})

    def _post_message(self, message: dict) -> dict:
        payload = json.dumps({"to": self.talk_id, "messages": [message]})
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.channel_access_token}"}
        response = requests.request("POST", self.MESSAGE_PUSH_API, headers=headers, data=payload)
        if response.status_code != 200:
            print(f"LINE API Error, status_code: {response.status_code}")
            print(response.json())
            raise Exception("LINE API Error")
        return response.json()


if __name__ == "__main__":
    # python -m notion_api.util.line.line_client
    line_client = LineClient.get_instance()
    line_client.push_message("hello")
