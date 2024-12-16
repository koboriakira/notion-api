from datetime import date, timedelta
from enum import Enum

from slack_sdk import WebClient

from util.datetime import jst_today
from zettlekasten.domain.zettlekasten import Zettlekasten
from zettlekasten.domain.zettlekasten_repository import ZettlekastenRepository


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
    SLACK_CHANNEL = "C05F6AASERZ"
    BEFORE_3_DAYS = jst_today() - timedelta(days=3)
    BEFORE_7_DAYS = jst_today() - timedelta(days=7)
    BEFORE_30_DAYS = jst_today() - timedelta(days=30)

    def __init__(self, zettlekasten_repository: ZettlekastenRepository, slack_client: WebClient) -> None:
        self._zettlekasten_repository = zettlekasten_repository
        self._slack_client = slack_client

    def execute(self) -> None:
        zettlekastens = self._zettlekasten_repository.fetch_all()

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

    from lotion import Lotion

    from zettlekasten.infrastructure.zettlekasten_repository_impl import ZettlekastenRepositoryImpl

    repository = ZettlekastenRepositoryImpl(client=Lotion.get_instance())
    use_case = RemindZettlekastenUseCase(
        zettlekasten_repository=repository,
        slack_client=WebClient(token=os.environ["SLACK_BOT_TOKEN"]),
    )
    use_case.execute()
