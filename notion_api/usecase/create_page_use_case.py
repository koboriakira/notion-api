from logging import Logger

from common.value.site_kind import SiteKind
from injector.page_creator_factory import PageCreatorFactory
from slack_concierge.service.append_context_service import AppendContextService
from usecase.service.inbox_service import InboxService


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
        site_kind = SiteKind.find_site_kind(url=url)
        page_creator = self._page_creator_factory.get_creator(url=url)
        self._logger.debug(f"site_kind={site_kind.value}, page_creator={type(page_creator)}")
