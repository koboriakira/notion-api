import os
from typing import Optional
from datetime import date as DateObject
from datetime import timedelta
from datetime import datetime as Datetime
from notion_client_wrapper.properties import Title, Date, Relation
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.client_wrapper import ClientWrapper
from domain.database_type import DatabaseType


class CreateNewTaskUsecase:
    def __init__(self):
        self.client = ClientWrapper(notion_secret=os.getenv("NOTION_SECRET"))

    def handle(self, title: Optional[str], mentioned_page_id: Optional[str], start_date: Optional[DateObject] = None) -> dict:
        if title is None and mentioned_page_id is None:
            raise ValueError("title と mentioned_page_id のどちらかは必須です")

        title = self._generate_title(title=title, mentioned_page_id=mentioned_page_id)
        properties = [title]
        if start_date is not None:
            properties.append(Date.from_start_date(name="実施日", start_date=start_date))

        page = self.client.create_page_in_database(
            database_id=DatabaseType.TASK.value,
            properties=properties)

        return {
            "id": page["id"],
            "url": page["url"],
        }

    def _generate_title(self, title: Optional[str], mentioned_page_id: Optional[str]) -> Title:
        if mentioned_page_id is None:
            return Title.from_plain_text(name="名前", text=title)
        if mentioned_page_id is not None:
            return Title.from_mentioned_page_id(name="名前", page_id=mentioned_page_id)
        raise NotImplementedError()



    def _find_weekly_log(self, year: int, isoweeknum: int) -> Optional[dict]:
        title=f"{year}-Week{isoweeknum}"
        weekly_logs = self.client.retrieve_database(
            database_id=DatabaseType.WEEKLY_LOG.value,
            title=title
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
            ]
        )

    def _find_daily_log(self, date: DateObject) -> Optional[BasePage]:
        daily_logs = self.client.retrieve_database(
            database_id=DatabaseType.DAILY_LOG.value,
            title=date.isoformat()
        )
        if len(daily_logs) == 0:
            return None
        return daily_logs[0]

    def _create_daily_log_page(self, date: DateObject, weekly_log_id: str) -> dict:
        return self.client.create_page_in_database(
            database_id=DatabaseType.DAILY_LOG.value,
            properties=[
                Date.from_start_date(name="日付", start_date=date),
                Title.from_plain_text(name="名前", text=date.isoformat()),
                Relation.from_id_list(name="💭 ウィークリーログ", id_list=[weekly_log_id])]
        )

if __name__ == "__main__":
    # python -m usecase.create_daily_log_usecase
    usecase = CreateDailyLogUsecase()
    usecase.handle(year=2024, isoweeknum=3)
