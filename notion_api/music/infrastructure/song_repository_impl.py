from logging import Logger, getLogger

from common.value.database_type import DatabaseType
from music.domain.song import Song
from music.domain.song_repository import SongRepository
from music.domain.song_title import SongTitle
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.filter_builder import FilterBuilder


class SongRepositoryImpl(SongRepository):
    DATABASE_ID = DatabaseType.MUSIC.value

    def __init__(self, client: ClientWrapper, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

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
