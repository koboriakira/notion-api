from logging import Logger, getLogger
from typing import cast

from common.value.database_type import DatabaseType
from music.domain.song import Song
from music.domain.song_repository import SongRepository
from music.domain.song_title import SongTitle
from notion_client_wrapper.base_page import BasePage
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.condition.date_condition import DateCondition, DateConditionType
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from util.date_range import DateRange


class SongRepositoryImpl(SongRepository):
    DATABASE_ID = DatabaseType.MUSIC.value

    def __init__(self, client: ClientWrapper, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def search(self, insert_datetime_range: DateRange) -> list[Song]:
        filter_builder = FilterBuilder()
        filter_builder = filter_builder.add_condition(
            DateCondition.create_manually(
                name="最終更新日時",
                condition_type=DateConditionType.ON_OR_AFTER,
                value=insert_datetime_range.start.value,
            ),
        )
        filter_builder = filter_builder.add_condition(
            DateCondition.create_manually(
                name="最終更新日時",
                condition_type=DateConditionType.ON_OR_BEFORE,
                value=insert_datetime_range.end.value,
            ),
        )
        base_pages = self._client.retrieve_database(database_id=self.DATABASE_ID, filter_param=filter_builder.build())
        return [self._cast(base_page) for base_page in base_pages]

    def find_by_title(self, title: str) -> Song | None:
        title_property = SongTitle(text=title)
        filter_param = FilterBuilder.build_simple_equal_condition(title_property)
        searched_songs = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=filter_param,
            page_model=Song,
        )
        if len(searched_songs) == 0:
            return None
        if len(searched_songs) > 1:
            warning_message = f"Found multiple songs with the same title: {title}"
            self._logger.warning(warning_message)
        return searched_songs[0]

    def save(self, song: Song) -> Song:
        result = self._client.create_page_in_database(
            database_id=self.DATABASE_ID,
            cover=song.cover,
            properties=song.properties.values,
        )
        song.update_id_and_url(
            page_id=result["id"],
            url=result["url"],
        )
        return song

    def _cast(self, base_page: BasePage) -> Song:
        return cast(Song, base_page)
