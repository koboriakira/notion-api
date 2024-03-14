import os
from datetime import date as DateObject
from datetime import datetime as Datetime
from datetime import timedelta

import requests

from domain.database_type import DatabaseType
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Cover, Date, Relation, Title


class CreateDailyLogUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()

    def handle(self, year: int = DateObject.today().year, isoweeknum: int = DateObject.today().isocalendar()[1]):
        # ウィークリーログを作成
        weekly_log_entity = self._find_weekly_log(year, isoweeknum)
        if weekly_log_entity is None:
            weekly_log_entity = self._create_weekly_log_page(year, isoweeknum)

        # 開始日から終了日までのデイリーログを作成
        # 指定さらた年とISO週から開始日、終了日を取得
        start_date = Datetime.strptime(f"{year}-{isoweeknum}-1", "%G-%V-%u")
        # datetimeをdateに変換
        start_date = Datetime.date(start_date)
        for i in range(7):
            daily_date = start_date + timedelta(days=i)
            if (_daily_log := self._find_daily_log(daily_date)) is None:
                _created_daily_log = self._create_daily_log_page(date=daily_date,
                                                                  weekly_log_id=weekly_log_entity["id"])


    def _find_weekly_log(self, year: int, isoweeknum: int) -> dict | None:
        title=f"{year}-Week{isoweeknum}"
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
        title_text = f"{year}-Week{isoweeknum}"
        start_date = Datetime.strptime(
            f"{year}-{isoweeknum}-1", "%G-%V-%u")
        start_date = Datetime.date(start_date)
        end_date = start_date + timedelta(days=6)

        return self.client.create_page_in_database(
            database_id=DatabaseType.WEEKLY_LOG.value,
            properties=[
                Title.from_plain_text(
                    name="名前", text=title_text),
                Date.from_range(name="期間", start=start_date, end=end_date),
            ],
        )

    def _find_daily_log(self, date: DateObject) -> BasePage | None:
        daily_logs = self.client.retrieve_database(
            database_id=DatabaseType.DAILY_LOG.value,
            title=date.isoformat(),
        )
        if len(daily_logs) == 0:
            return None
        return daily_logs[0]

    def _create_daily_log_page(self, date: DateObject, weekly_log_id: str) -> dict:
        cover_url = get_random_photo_url()
        return self.client.create_page_in_database(
            database_id=DatabaseType.DAILY_LOG.value,
            cover=Cover.from_external_url(external_url=cover_url),
            properties=[
                Date.from_start_date(name="日付", start_date=date),
                Title.from_plain_text(name="名前", text=date.isoformat()),
                Relation.from_id_list(name="💭 ウィークリーログ", id_list=[weekly_log_id])],
        )

def get_random_photo_url() -> str | None:
    query = "bird,flower"
    UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
    unsplash_api_url = f"https://api.unsplash.com/photos/random/?client_id={UNSPLASH_ACCESS_KEY}&query={query}"
    response = requests.get(unsplash_api_url)
    if response.status_code != 200:
        return None
    data = response.json()
    return data["urls"]["full"]



if __name__ == "__main__":
    # python -m usecase.create_daily_log_usecase
    usecase = CreateDailyLogUsecase()
    # usecase.handle(year=2024, isoweeknum=3)
    print(get_random_photo_url())
