import json
import logging

from injector.injector import Injector
from usecase.add_video_usecase import AddVideoUsecase
from usecase.create_page_use_case import CreatePageRequest
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def execute(request_param: CreatePageRequest) -> dict:
    usecase = Injector.create_page_use_case()
    return usecase.execute(request_param=request_param)


def handler(event:dict, context:dict) -> dict:  # noqa: ARG001
    request: dict = json.loads(event["Records"][0]["body"])
    print("request", request)
    mode: str = request["mode"]
    request_param = CreatePageRequest.from_params(request["params"])
    try:
        if mode == "video":
            usecase = AddVideoUsecase()
            _ = usecase.execute(
                url=request_param.url,
                title=request_param.title,
                cover=request_param.cover,
                slack_channel=request_param.slack_channel,
                slack_thread_ts=request_param.slack_thread_ts,
                )
            return {}

        # いずれは上記2つもここに統合する
        execute(request_param)
        return {}
    except Exception:  # noqa: BLE001
        ErrorReporter().execute(
            slack_channel=request_param.slack_channel,
            slack_thread_ts=request_param.slack_thread_ts,
    )

if __name__ == "__main__":
    # python -m notion_api.create_page
    execute(url="https://tabelog.com/tokyo/A1305/A130501/13242384/", title="コイティー サンシャインシティアルパ店")
