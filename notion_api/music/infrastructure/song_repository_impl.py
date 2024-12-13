from logging import Logger, getLogger

from common.value.database_type import DatabaseType
from music.domain.song import Song
from music.domain.song_repository import SongRepository
from music.domain.spotify_url import SpotifyUrl
from lotion.base_page import BasePage
from lotion import Lotion
from notion_client_wrapper.filter.condition.date_condition import DateCondition, DateConditionType
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from util.date_range import DateRange


class SongRepositoryImpl(SongRepository):
    DATABASE_ID = DatabaseType.MUSIC.value

    def __init__(self, client: Lotion, logger: Logger | None = None) -> None:
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

    def find_by_url(self, url: str) -> Song | None:
        spotify_url = SpotifyUrl(url=url)
        filter_param = FilterBuilder.build_simple_equal_condition(spotify_url)
        searched_songs = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=filter_param,
            page_model=Song,
        )
        if len(searched_songs) == 0:
            return None
        if len(searched_songs) > 1:
            warning_message = f"Found multiple songs with the same url: {url}"
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
        return Song(
            properties=base_page.properties,
            block_children=base_page.block_children,
            id_=base_page.id_,
            url=base_page.url,
            created_time=base_page.created_time,
            last_edited_time=base_page.last_edited_time,
            created_by=base_page.created_by,
            last_edited_by=base_page.last_edited_by,
            cover=base_page.cover,
            icon=base_page.icon,
            archived=base_page.archived,
            parent=base_page.parent,
        )
