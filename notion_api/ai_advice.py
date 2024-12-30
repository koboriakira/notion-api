import logging

from task.task_repository_impl import TaskRepositoryImpl
from usecase.ai_advice_usecase import AiAdviceUsecase
from util.datetime import jst_now
from util.environment import Environment
from util.error_reporter import ErrorReporter

task_repository = TaskRepositoryImpl()
suite = AiAdviceUsecase(
    task_repository=task_repository,
)

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)


def handler(event: dict, context: dict) -> None:  # noqa: ARG001
    try:
        suite.execute(start_datetime=jst_now())
    except Exception as e:
        ErrorReporter().execute(error=e)
        raise


if __name__ == "__main__":
    # python -m notion_api.ai_advice
    handler({}, {})
