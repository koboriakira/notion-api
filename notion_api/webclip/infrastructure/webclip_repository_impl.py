from logging import Logger, getLogger

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.filter import Builder, Cond, Prop

from common.value.database_type import DatabaseType
from util.date_range import DateRange
from webclip.domain.webclip import Webclip
from webclip.domain.webclip_repository import WebclipRepository


class WebclipRepositoryImpl(WebclipRepository):
    DATABASE_ID = DatabaseType.WEBCLIP.value

    def __init__(self, client: Lotion, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def find_by_title(self, title: str) -> Webclip | None:
        builder = Builder.create().add(Prop.RICH_TEXT, "名前", Cond.EQUALS, title)
        base_pages = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=builder.build(),
        )
        if len(base_pages) == 0:
            return None
        if len(base_pages) > 1:
            warning_message = f"Found multiple webclips with the same title: {title}"
            self._logger.warning(warning_message)
        return self._cast(base_pages[0])

    def save(self, webclip: Webclip) -> Webclip:
        result = self._client.create_page_in_database(
            database_id=DatabaseType.WEBCLIP.value,
            properties=webclip.properties.values,
        )
        self._client.append_blocks(
            block_id=result.id,
            blocks=webclip.block_children,
        )
        webclip.update_id_and_url(
            page_id=result.id,
            url=result.url,
        )
        return webclip

    def search(self, date_range: DateRange) -> list[Webclip]:
        builder = (
            Builder.create()
            .add_last_edited_at(Cond.ON_OR_AFTER, date_range.start.value.isoformat())
            .add_last_edited_at(
                Cond.ON_OR_BEFORE,
                date_range.end.value.isoformat(),
            )
        )
        base_pages = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=builder.build(),
        )
        return [self._cast(base_page) for base_page in base_pages]

    def _cast(self, base_page: BasePage) -> Webclip:
        return Webclip(
            properties=base_page.properties,
            block_children=base_page.block_children,
            id_=base_page.id_,
            url_=base_page.url,
            created_time=base_page.created_time,
            last_edited_time=base_page.last_edited_time,
            _created_by=base_page._created_by,
            _last_edited_by=base_page._last_edited_by,
            cover=base_page.cover,
            icon=base_page.icon,
            archived=base_page.archived,
            parent=base_page.parent,
        )
