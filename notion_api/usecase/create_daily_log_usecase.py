import os
from datetime import date, datetime, timedelta

import requests

from common.value.database_type import DatabaseType
from daily_log.domain.daily_log_builder import DailyLogBuilder
from daily_log.domain.daily_log_repository import DailyLogRepository
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.page.page_id import PageId
from notion_client_wrapper.properties import Date, Title
from util.datetime import JST, jst_today


class CreateDailyLogUsecase:
    def __init__(self, client: ClientWrapper, daily_log_repository: DailyLogRepository) -> None:
        self.client = client
        self._daily_log_repository = daily_log_repository

    def handle(self, year: int | None = None, isoweeknum: int | None = None) -> None:
        # 初期化
        year = year or jst_today().year
        isoweeknum = isoweeknum or jst_today().isocalendar()[1]

        # ウィークリーログを作成
        weekly_log_entity = self._create_weekly_log_page(year, isoweeknum)
        weekly_log_id = weekly_log_entity["id"]

        # 開始日から終了日までのデイリーログを作成
        # 指定さらた年とISO週から開始日、終了日を取得
        start_date = generate_date(year, isoweeknum)
        for i in range(7):
            daily_date = start_date + timedelta(days=i)
            self._create_daily_log_page(date_=daily_date, weekly_log_id=weekly_log_id)

    def _find_weekly_log(self, year: int, isoweeknum: int) -> dict | None:
        title = f"{year}-Week{isoweeknum}"
        weekly_logs = self.client.retrieve_database(
            database_id=DatabaseType.WEEKLY_LOG.value,
            title=title,
        )
        if len(weekly_logs) == 0:
            return None

        weekly_log = weekly_logs[0]
        title = weekly_log.get_title()
        goal = weekly_log.get_text(name="目標")

        return {
            "id": weekly_log.id,
            "url": weekly_log.url,
            "title": title.text,
            "goal": goal.text,
        }

    def _create_weekly_log_page(self, year: int, isoweeknum: int) -> dict:
        weekly_log_entity = self._find_weekly_log(year, isoweeknum)
        if weekly_log_entity is not None:
            return weekly_log_entity

        title_text = f"{year}-Week{isoweeknum}"
        start_date = generate_date(year, isoweeknum)
        end_date = start_date + timedelta(days=6)

        return self.client.create_page_in_database(
            database_id=DatabaseType.WEEKLY_LOG.value,
            properties=[
                Title.from_plain_text(name="名前", text=title_text),
                Date.from_range(name="期間", start=start_date, end=end_date),
            ],
        )

    def _create_daily_log_page(self, date_: date, weekly_log_id: str) -> None:
        daily_log = self._daily_log_repository.find(date_)
        if daily_log is not None:
            return

        yesterday_daily_log = self._daily_log_repository.find(date_ - timedelta(days=1))
        if yesterday_daily_log is None:
            msg = "前日のデイリーログが存在しません"
            raise ValueError(msg)

        cover_url = get_random_photo_url()

        daily_log = (
            DailyLogBuilder.of(date_=date_)
            .add_weekly_log_relation(weekly_log_page_id=PageId(weekly_log_id))
            .add_previous_relation(previous_page_id=PageId(yesterday_daily_log.id))
            .add_cover(cover_url=cover_url)
            .build()
        )
        self._daily_log_repository.save(daily_log)


def generate_date(year: int, isoweeknum: int) -> date:
    return datetime.strptime(f"{year}-{isoweeknum}-1", "%G-%V-%u").replace(tzinfo=JST).date()


def get_random_photo_url() -> str | None:
    query = "bird,flower"
    unsplash_access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    unsplash_api_url = f"https://api.unsplash.com/photos/random/?client_id={unsplash_access_key}&query={query}"
    response = requests.get(unsplash_api_url, timeout=15)
    if response.status_code != 200:
        return None
    data = response.json()
    return data["urls"]["full"]
