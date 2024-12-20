from logging import Logger, getLogger

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.filter import Builder
from lotion.filter.condition import Cond, Prop

from common.value.database_type import DatabaseType
from music.domain.song import Song
from music.domain.song_repository import SongRepository
from music.domain.spotify_url import SpotifyUrl
from util.date_range import DateRange


class SongRepositoryImpl(SongRepository):
    DATABASE_ID = DatabaseType.MUSIC.value

    def __init__(self, client: Lotion, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def search(self, insert_datetime_range: DateRange) -> list[Song]:
        builder = (
            Builder.create()
            .add_created_at(Cond.ON_OR_AFTER, insert_datetime_range.start.value.isoformat())
            .add_created_at(
                Cond.ON_OR_BEFORE,
                insert_datetime_range.end.value.isoformat(),
            )
        )
        base_pages = self._client.retrieve_database(database_id=self.DATABASE_ID, filter_param=builder.build())
        return [self._cast(base_page) for base_page in base_pages]

    def find_by_url(self, url: str) -> Song | None:
        builder = Builder.create().add(Prop.RICH_TEXT, SpotifyUrl.NAME, Cond.EQUALS, url)
        searched_songs = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=builder.build(),
        )
        if len(searched_songs) == 0:
            return None
        if len(searched_songs) > 1:
            warning_message = f"Found multiple songs with the same url: {url}"
            self._logger.warning(warning_message)
        return self._cast(searched_songs[0])

    def save(self, song: Song) -> Song:
        result = self._client.create_page_in_database(
            database_id=self.DATABASE_ID,
            cover=song.cover,
            properties=song.properties.values,
        )
        song.update_id_and_url(
            page_id=result.id,
            url=result.url,
        )
        return song

    def _cast(self, base_page: BasePage) -> Song:
        return Song(
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
