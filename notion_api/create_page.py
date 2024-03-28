import json
import logging

from injector.injector import Injector
from usecase.create_page_use_case import CreatePageRequest
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

def execute(request: CreatePageRequest) -> dict:
    usecase = Injector.create_page_use_case()
    return usecase.execute(request=request)


def handler(event:dict, context:dict) -> dict:  # noqa: ARG001
    body: dict = json.loads(event["Records"][0]["body"])
    print("body", body)
    request = CreatePageRequest.from_params(body["params"])
    try:
        execute(request)
        return {}
    except Exception:  # noqa: BLE001
        ErrorReporter().execute(
            slack_channel=request.slack_channel,
            slack_thread_ts=request.slack_thread_ts,
    )

if __name__ == "__main__":
    # python -m notion_api.create_page
    request = CreatePageRequest(
        url="https://tabelog.com/tokyo/A1305/A130501/13242384/",
        title="コイティー サンシャインシティアルパ店",

    )
    execute(request=request)
