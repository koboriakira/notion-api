from datetime import date
from logging import getLogger

from daily_log.infrastructure.daily_log_repository_impl import DailyLogRepositoryImpl
from notion_client_wrapper.client_wrapper import ClientWrapper
from usecase.create_daily_log_usecase import CreateDailyLogUsecase
from util.datetime import jst_now


def create_daily_log(target_date: date | None = None) -> None:
    client = ClientWrapper.get_instance()
    daily_log_repository = DailyLogRepositoryImpl(client=client, logger=getLogger(__name__))

    target_date = target_date or jst_now()
    usecase = CreateDailyLogUsecase(
        client=client,
        daily_log_repository=daily_log_repository,
    )
    usecase.handle(
        year=target_date.year,
        isoweeknum=target_date.isocalendar()[1],
    )
