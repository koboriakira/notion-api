from datetime import date

from music.domain.artist import Artist
from music.domain.release_date import ReleaseDate
from music.domain.song import Song
from music.domain.song_title import SongTitle
from music.domain.spotify_url import SpotifyUrl
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.properties import Properties


class SongFactory:
    @classmethod
    def create_spotify_song(
        cls,
        title: str,
        spotify_url: str,
        cover_url: str,
        artists: list[str],
        release_date: date | None = None,
    ) -> Song:
        properties = [
            SongTitle(text=title),
            SpotifyUrl(url=spotify_url),
            Artist.from_str_list(artists),
        ]
        if release_date is not None:
            properties.append(ReleaseDate(release_date))
        return Song(
            properties=Properties(values=properties),
            cover=Cover.from_external_url(external_url=cover_url),
            block_children=[],
        )
