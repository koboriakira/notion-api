import logging
import json
from util.environment import Environment
from interface import video, webclip

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def handler(event, context):
    print("event", event)
    print("records", event["Records"])
    request:dict = json.loads(event["Records"][0]["body"])
    print("request", request)
    params: dict = request["params"]
    if request["mode"] == "video":
        video.add_page(
            url=params["url"],
            title=params["title"],
            cover=params.get("cover") or None,
            slack_channel=params.get("slack_channel") or None,
            slack_thread_ts=params.get("slack_thread_ts") or None,
        )
    if request["mode"] == "webclip":
        webclip.add_page(
            url=params["url"],
            title=params["title"],
            cover=params.get("cover") or None,
            slack_channel=params.get("slack_channel") or None,
            slack_thread_ts=params.get("slack_thread_ts") or None,
        )
