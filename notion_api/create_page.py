import logging
import json
from util.environment import Environment
from interface import video


# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def handler(event, context):
    print("event", event)
    print("records", event["Records"])
    request:dict = json.loads(event["Records"][0]["body"])
    print("request", request)
    params = request["params"]
    if request["mode"] == "video":
        video.add_page(
            url=params["url"],
            title=params["title"],
            tags=params["tags"] if "tags" in params else [],
            cover=params.get("cover") or None,
        )
