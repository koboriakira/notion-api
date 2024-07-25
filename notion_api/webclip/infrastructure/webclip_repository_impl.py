from logging import Logger, getLogger

from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.database.database_type import DatabaseType
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_client_wrapper.properties.title import Title
from webclip.domain.webclip import Webclip


class WebclipRepositoryImpl:
    def __init__(self, client: ClientWrapper, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def find_by_title(self, title: str) -> Webclip | None:
        title_property = Title.from_plain_text(name="名前", text=title)
        filter_param = FilterBuilder.build_simple_equal_condition(title_property)
        searched_webclips: list[Webclip] = self._client.retrieve_database(
            database_id=DatabaseType.WEBCLIP.value,
            filter_param=filter_param,
            page_model=Webclip,
        )
        if len(searched_webclips) == 0:
            return None
        if len(searched_webclips) > 1:
            warning_message = f"Found multiple webclips with the same title: {title}"
            self._logger.warning(warning_message)
        return searched_webclips[0]

    def save(self, webclip: Webclip) -> Webclip:
        result = self._client.create_page_in_database(
            database_id=DatabaseType.WEBCLIP.value,
            properties=webclip.properties.values,
        )
        self._client.append_blocks(
            block_id=result["id"],
            blocks=webclip.block_children,
        )
        webclip.update_id_and_url(
            page_id=result["id"],
            url=result["url"],
        )
        return webclip
