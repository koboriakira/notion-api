import json
import logging

from infrastructure.slack_bot_client import SlackBotClient
from interface import video, webclip
from util.environment import Environment

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)


def find_request(event: dict) -> dict:
    try:
        return json.loads(event["Records"][0]["body"])
    except Exception:
        print("event", event)
        print("records", event["Records"])
        raise


def handler(event, context):
    request: dict = json.loads(event["Records"][0]["body"])
    print("request", request)
    mode: str = request["mode"]
    params: dict = request["params"]
    try:
        if mode == "video":
            video.add_page(
                url=params["url"],
                title=params["title"],
                cover=params.get("cover") or None,
                slack_channel=params.get("slack_channel") or None,
                slack_thread_ts=params.get("slack_thread_ts") or None,
            )
        if mode == "webclip":
            webclip.add_page(
                url=params["url"],
                title=params["title"],
                cover=params.get("cover") or None,
                slack_channel=params.get("slack_channel") or None,
                slack_thread_ts=params.get("slack_thread_ts") or None,
            )
    except Exception as e:
        slack_bot_client = SlackBotClient()
        error_message = f"エラーが発生しました: {e}"
        slack_bot_client.send_message(channel="C04Q3AV4TA5", text=error_message)
