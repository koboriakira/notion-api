import json
import logging

from injector.injector import Injector
from usecase.add_video_usecase import AddVideoUsecase
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def execute(  # noqa: PLR0913
        url: str,
        title: str | None = None,
        cover: str | None = None,
        slack_channel: str | None = None,
        slack_thread_ts: str | None = None,
        params: dict|None = None, # いつか使うかも  # noqa: ARG001
        ) -> dict:
    usecase = Injector.create_page_use_case()
    return usecase.execute(url=url, title=title, cover=cover, slack_channel=slack_channel, slack_thread_ts=slack_thread_ts)


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
            return {}
        if mode == "webclip":
            usecase = Injector.create_add_webclip_usecase()
            _ = usecase.execute(
                url=params["url"],
                title=params["title"],
                cover=params.get("cover"),
                slack_channel=slack_channel,
                slack_thread_ts=slack_thread_ts,
            )
            return {}

        # いずれは上記2つもここに統合する
        execute(
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

if __name__ == "__main__":
    # python -m notion_api.create_page
    execute(url="https://tabelog.com/tokyo/A1305/A130501/13242384/", title="コイティー サンシャインシティアルパ店")
