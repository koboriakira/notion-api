from dataclasses import dataclass
from datetime import date
from logging import Logger, getLogger

from common.service.page_creator import PageCreator
from music.domain.song import Song
from music.domain.song_repository import SongRepository
from music.service.song_factory import SongFactory


@dataclass
class _MusicRequestParam:
    artists: list[str]
    release_date: date | None

    @staticmethod
    def from_params(
        params: dict | None,
    ) -> "_MusicRequestParam":
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
        song_repository: SongRepository,
        logger: Logger | None = None,
    ) -> None:
        self._song_repository = song_repository
        self._logger = logger or getLogger(__name__)

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

        song = self._song_repository.find_by_title(title=title)
        if song is not None:
            info_message = f"The song is already registered: {song.get_title_text()}"
            self._logger.info(info_message)
            return song

        info_message = "Create a Music"
        self._logger.info(info_message)

        request_params = _MusicRequestParam.from_params(params)
        song = SongFactory.create_spotify_song(
            title=title,
            spotify_url=url,
            cover_url=cover,
            artists=request_params.artists,
            release_date=request_params.release_date,
        )
        return self._song_repository.save(song)
