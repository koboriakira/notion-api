from datetime import date

from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.block import Block
from lotion.properties import Cover, Date, Text, Title

from common.domain.tag_relation import TagRelation
from common.value.database_type import DatabaseType
from music.domain.spotify_url import SpotifyUrl


@notion_prop("Artist")
class Artist(Text):
    @staticmethod
    def from_str_list(str_list: list[str]) -> "Artist":
        return Artist.from_plain_text(text=", ".join(str_list))

    @staticmethod
    def from_str(artists: str) -> "Artist":
        return Artist.from_str_list(artists.split(","))


@notion_prop("名前")
class SongTitle(Title):
    pass


@notion_prop("リリース日")
class ReleaseDate(Date):
    pass


@notion_database(DatabaseType.MUSIC.value)
class Song(BasePage):
    title: SongTitle
    release_date: ReleaseDate
    artist: Artist
    spotify_url: SpotifyUrl
    tags: TagRelation

    @staticmethod
    def generate(  # noqa: PLR0913
        title: str,
        artist: str | list[str],
        spotify_url: str | None = None,
        tag_relation: list[str] | None = None,
        release_date: date | None = None,
        blocks: list[Block] | None = None,
        cover: str | None = None,
    ) -> "Song":
        blocks = blocks or []
        properties = [
            SongTitle.from_plain_text(title),
            Artist.from_str(artist) if isinstance(artist, str) else Artist.from_str_list(artist),
        ]
        if spotify_url is not None:
            properties.append(SpotifyUrl.from_url(spotify_url))
        if tag_relation is not None:
            properties.append(TagRelation.from_id_list(tag_relation))

        if release_date is not None:
            properties.append(ReleaseDate.from_start_date(release_date))

        if cover is None:
            return Song.create(properties, blocks)
        return Song.create(properties, blocks, cover=Cover.from_external_url(cover))
