from abc import ABCMeta, abstractmethod

from music.domain.song import Song
from util.date_range import DateRange


class SongRepository(metaclass=ABCMeta):
    @abstractmethod
    def search(self, insert_datetime_range: DateRange) -> list[Song]:
        """Search songs by insert datetime range."""

    @abstractmethod
    def find_by_url(self, url: str) -> Song | None:
        """Find a song by title."""

    @abstractmethod
    def save(self, song: Song) -> Song:
        """Save a song."""
