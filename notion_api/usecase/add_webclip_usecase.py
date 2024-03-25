
from slack_concierge.service.append_context_service import AppendContextService
from usecase.service.inbox_service import InboxService
from webclip.service.webclip_creator import WebclipCreator


class AddWebclipUsecase:
    def __init__(
            self,
            webclip_creator: WebclipCreator,
            inbox_service: InboxService,
            append_context_service: AppendContextService,
            ) -> None:
        self._webclip_creator = webclip_creator
        self._inbox_service = inbox_service
        self._append_context_service = append_context_service

    def execute(  # noqa: PLR0913
            self,
            url: str,
            title: str,
            cover: str | None = None,
            slack_channel: str | None = None,
            slack_thread_ts: str | None = None,
            ) -> dict:
        # Webclipページを作成
        webclip = self._webclip_creator.execute(
            url=url,
            title=title,
            cover=cover,
        )

        # Inboxにタスクを追加
        self._inbox_service.add_inbox_task_by_page_id(
            page_id=webclip.id,
            page_url=webclip.url,
            original_url=url,
            slack_channel=slack_channel,
            slack_thread_ts=slack_thread_ts,
        )

        # コンテキストにページIDを追加
        self._append_context_service.append_page_id(
            channel=slack_channel,
            event_ts=slack_thread_ts,
            page_id=webclip.id,
        )

        return {
            "id": webclip.id,
            "url": webclip.url,
        }

if __name__ == "__main__":
    # python -m notion_api.usecase.add_webclip_usecase
    from injector.injector import Injector
    usecase = Injector.create_add_webclip_usecase()
    usecase.execute(
        url="https://speakerdeck.com/yuitosato/functional-and-type-safe-ddd-for-oop",
        title="ビジネスロジックを「型」で表現するOOPのための関数型DDD / Functional And Type-Safe DDD for OOP",
        slack_channel="C05GUTE35RU",
        slack_thread_ts="1711238809.901419",
    )
