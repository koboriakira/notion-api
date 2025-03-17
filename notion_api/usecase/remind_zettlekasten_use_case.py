from datetime import date, timedelta
from enum import Enum

from lotion import Lotion
from slack_sdk import WebClient

from common.value.slack_channel_type import ChannelType
from notion_databases.zettlekasten import Zettlekasten
from util.datetime import jst_today


class PastDays(Enum):
    THREE_DAYS = 3
    SEVEN_DAYS = 7
    THIRTY_DAYS = 30

    def __str__(self) -> str:
        return f"{self.value}日経過"


"""
定期的にZettlekastenのリマインドを行うユースケース
"""


class RemindZettlekastenUseCase:
    SLACK_CHANNEL = ChannelType.NOTIFICATION.value
    BEFORE_3_DAYS = jst_today() - timedelta(days=3)
    BEFORE_7_DAYS = jst_today() - timedelta(days=7)
    BEFORE_30_DAYS = jst_today() - timedelta(days=30)

    def __init__(self, slack_client: WebClient, lotion: Lotion | None = None) -> None:
        self._slack_client = slack_client
        self._lotion = lotion or Lotion.get_instance()

    def execute(self) -> None:
        zettlekastens = self._lotion.retrieve_pages(Zettlekasten)

        for zettlekasten in zettlekastens:
            self._print_if_specified_date(zettlekasten)

    def _print_if_specified_date(self, zettlekasten: Zettlekasten) -> None:
        print(zettlekasten)
        created_date = zettlekasten.created_at.date()
        past_days = self._calculate_past_days(created_date)
        if past_days is None:
            return
        self._send_slack_message(zettlekasten, past_days=past_days)

    def _calculate_past_days(self, created_date: date) -> PastDays | None:
        if created_date == self.BEFORE_3_DAYS:
            return PastDays.THREE_DAYS
        if created_date == self.BEFORE_7_DAYS:
            return PastDays.SEVEN_DAYS
        if created_date == self.BEFORE_30_DAYS:
            return PastDays.THIRTY_DAYS
        return None

    def _send_slack_message(self, zettlekasten: Zettlekasten, past_days: PastDays) -> None:
        text = f"{past_days!s}: {zettlekasten.title_for_slack()}"
        self._slack_client.chat_postMessage(channel=self.SLACK_CHANNEL, text=text)


if __name__ == "__main__":
    # python -m notion_api.usecase.remind_zettlekasten_use_case
    import os

    use_case = RemindZettlekastenUseCase(
        slack_client=WebClient(token=os.environ["SLACK_BOT_TOKEN"]),
    )
    use_case.execute()
