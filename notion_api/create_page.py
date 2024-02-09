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
    video.add_page(
        url=request["url"],
        title=request["title"],
        tags=request["tags"] if "tags" in request else [],
        cover=request.get("cover"),
    )
