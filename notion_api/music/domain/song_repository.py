from abc import ABCMeta, abstractmethod

from music.domain.song import Song


class SongRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_title(self, title: str) -> Song | None:
        """Find a song by title."""

    @abstractmethod
    def save(self, song: Song) -> Song:
        """Save a song."""
