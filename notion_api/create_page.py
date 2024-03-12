import json
import logging

from infrastructure.slack_user_client import SlackUserClient
from usecase.add_video_usecase import AddVideoUsecase
from usecase.add_webclip_usecase import AddWebclipUsecase
from usecase.service.error_reporter import ErrorReporter
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


def handler(event:dict, context:dict) -> dict:  # noqa: ARG001
    request: dict = json.loads(event["Records"][0]["body"])
    print("request", request)
    mode: str = request["mode"]
    params: dict = request["params"]
    slack_channel=params.get("slack_channel")
    slack_thread_ts=params.get("slack_thread_ts")
    try:
        result_page_id = None
        if mode == "video":
            usecase = AddVideoUsecase()
            result = usecase.execute(
                url=params["url"],
                title=params["title"],
                cover=params.get("cover"),
                slack_channel=slack_channel,
                slack_thread_ts=slack_thread_ts,
                )
            result_page_id = result["id"]
        if mode == "webclip":
            usecase = AddWebclipUsecase()
            result = usecase.execute(
                url=params["url"],
                title=params["title"],
                cover=params.get("cover"),
                slack_channel=slack_channel,
                slack_thread_ts=slack_thread_ts,
            )
            result_page_id = result["id"]
        if slack_channel and slack_thread_ts:
            slack_user_client = SlackUserClient()
            slack_user_client.update_context(
                channel=slack_channel,
                ts=slack_thread_ts,
                context={
                    "page_id": result_page_id,
                },
            )
        return {}
    except Exception as e:  # noqa: BLE001
        ErrorReporter().report_error(
            err=e,
            channel=slack_channel,
            thread_ts=slack_thread_ts,
    )
