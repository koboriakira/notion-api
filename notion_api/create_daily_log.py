import logging

from daily_log.infrastructure.daily_log_repository_impl import DailyLogRepositoryImpl
from daily_log.value.isoweek import Isoweek
from notion_client_wrapper.client_wrapper import ClientWrapper
from usecase.create_daily_log_usecase import CreateDailyLogUsecase
from util.datetime import jst_now
from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)


def handler(event: dict, context: dict) -> None:  # noqa: ARG001
    try:
        client = ClientWrapper.get_instance()
        daily_log_repository = DailyLogRepositoryImpl(client=client, logger=logging.getLogger(__name__))

        usecase = CreateDailyLogUsecase(
            client=client,
            daily_log_repository=daily_log_repository,
        )
        isoweek = Isoweek.of(date_=jst_now())
        usecase.handle(isoweek=isoweek)

    except:
        ErrorReporter().execute()
        raise


if __name__ == "__main__":
    # python -m notion_api.create_daily_log
    handler({}, {})
