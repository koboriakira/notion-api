from dataclasses import dataclass
from datetime import date
from logging import Logger, getLogger

from lotion import Lotion
from lotion.filter import Builder, Cond

from common.service.page_creator import PageCreator
from notion_databases.song import Song
from notion_databases.song_prop.spotify_url import SpotifyUrl


@dataclass
class _MusicRequestParam:
    artists: list[str]
    release_date: date | None

    @staticmethod
    def from_params(
        params: dict | None,
    ) -> "_MusicRequestParam":
        if params is None:
            return _MusicRequestParam(artists=[], release_date=None)
        artists = params.get("artists", [])
        release_date = params.get("release_date", None)
        return _MusicRequestParam(
            artists=artists,
            release_date=date.fromisoformat(release_date)
            if release_date is not None and len(release_date) == 10  # noqa: PLR2004
            else None,
        )


class MusicCreator(PageCreator):
    def __init__(
        self,
        logger: Logger | None = None,
    ) -> None:
        self._logger = logger or getLogger(__name__)
        self._lotion = Lotion.get_instance()

    def execute(
        self,
        url: str,
        title: str | None = None,
        cover: str | None = None,
        params: dict | None = None,
    ) -> Song:
        if title is None:
            msg = "title is required"
            raise ValueError(msg)

        info_message = f"{self.__class__} execute: url={url}, title={title}, cover={cover}"
        self._logger.info(info_message)

        spotify_url = SpotifyUrl.from_url(url)
        builder = Builder.create().add(spotify_url, Cond.EQUALS)
        searched_songs = self._lotion.retrieve_pages(
            cls=Song,
            filter_param=builder.build(),
        )
        if len(searched_songs) > 0:
            song = searched_songs[0]
            info_message = f"The song is already registered: {song.get_title_text()}"
            self._logger.info(info_message)
            return searched_songs[0]

        info_message = "Create a Music"
        self._logger.info(info_message)

        request_params = _MusicRequestParam.from_params(params)
        song = Song.generate(
            title=title,
            spotify_url=url,
            cover=cover,
            artist=request_params.artists,
            release_date=request_params.release_date,
        )
        return self._lotion.update(song)
