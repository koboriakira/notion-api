
from domain.database_type import DatabaseType
from infrastructure.slack_bot_client import SlackBotClient
from infrastructure.slack_user_client import SlackUserClient
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Title


class InboxService:
    def __init__(self) -> None:
        self.client = ClientWrapper.get_instance()
        self.slack_bot_client = SlackBotClient()
        self.slack_user_client = SlackUserClient()

    def add_inbox_task_by_page_id(self, page_id: str, page_url: str, slack_channel: str | None = None, slack_thread_ts: str | None = None) -> None:
        """ Notionの他ページに関連するタスクを追加する """
        title = Title.from_mentioned_page_id(name="名前", page_id=page_id)
        _page = self.client.create_page_in_database(
            database_id=DatabaseType.TASK.value,
            properties=[title])
        if slack_channel is not None:
            self.slack_bot_client.send_message(
                channel=slack_channel,
                text=f"ページを作成しました: {page_url}",
                thread_ts=slack_thread_ts,
            )
