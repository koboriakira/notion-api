import json
import logging

from common.service.scrape_service import ScrapeServiceInjector
from usecase.add_video_usecase import AddVideoUsecase
from usecase.add_webclip_usecase import AddWebclipUsecase
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)



def handler(event:dict, context:dict) -> dict:  # noqa: ARG001
    request: dict = json.loads(event["Records"][0]["body"])
    print("request", request)
    mode: str = request["mode"]
    params: dict = request["params"]
    slack_channel=params.get("slack_channel")
    slack_thread_ts=params.get("slack_thread_ts")
    try:
        if mode == "video":
            usecase = AddVideoUsecase()
            _ = usecase.execute(
                url=params["url"],
                title=params["title"],
                cover=params.get("cover"),
                slack_channel=slack_channel,
                slack_thread_ts=slack_thread_ts,
                )
        if mode == "webclip":
            scrape_service = ScrapeServiceInjector.get_instance()
            usecase = AddWebclipUsecase(
                scrape_service=scrape_service,
            )
            _ = usecase.execute(
                url=params["url"],
                title=params["title"],
                cover=params.get("cover"),
                slack_channel=slack_channel,
                slack_thread_ts=slack_thread_ts,
            )
        return {}
    except Exception:  # noqa: BLE001
        ErrorReporter().execute(
            slack_channel=slack_channel,
            slack_thread_ts=slack_thread_ts,
    )
