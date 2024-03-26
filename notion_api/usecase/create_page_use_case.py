from logging import Logger
from typing import TYPE_CHECKING

from common.value.site_kind import SiteKind
from injector.page_creator_factory import PageCreatorFactory
from slack_concierge.service.append_context_service import AppendContextService
from usecase.service.inbox_service import InboxService

if TYPE_CHECKING:
    from common.service.page_creator import PageCreator


class CreatePageUseCase:
    def __init__(
            self,
            page_creator_factory: PageCreatorFactory,
            inbox_service: InboxService,
            append_context_service: AppendContextService,
            logger: Logger,
            ) -> None:
        self._page_creator_factory = page_creator_factory
        self._inbox_service = inbox_service
        self._append_context_service = append_context_service
        self._logger = logger

    def execute(  # noqa: PLR0913
            self,
            url: str,
            title: str | None = None,
            cover: str | None = None,
            slack_channel: str | None = None,
            slack_thread_ts: str | None = None,
            ) -> dict:
        # どのデータベースのページを作るべきか判断して、作成する
        site_kind = SiteKind.find_site_kind(url=url)
        page_creator:PageCreator = self._page_creator_factory.get_creator(site_kind=site_kind)
        self._logger.debug(f"site_kind={site_kind.value}, page_creator={type(page_creator)}")
        page = page_creator.execute(url=url, title=title, cover=cover)

        # Inboxにタスクを追加
        self._inbox_service.add_inbox_task_by_page_id(
            page_id=page.id,
            page_url=page.url,
            original_url=url,
            slack_channel=slack_channel,
            slack_thread_ts=slack_thread_ts,
        )

        # コンテキストにページIDを追加
        self._append_context_service.append_page_id(
            channel=slack_channel,
            event_ts=slack_thread_ts,
            page_id=page.id,
        )

        return {
            "id": page.id,
            "url": page.url,
        }
