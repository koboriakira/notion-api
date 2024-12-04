from abc import ABCMeta, abstractmethod

from common.value.database_type import DatabaseType
from video.domain.video import Video


class VideoRepository(metaclass=ABCMeta):
    DATABASE_ID = DatabaseType.VIDEO.value


    @abstractmethod
    def find_by_title(self, title: str) -> Video | None:
        """Find a video by title"""

    @abstractmethod
    def save(self, video: Video) -> Video:
        """Save a video"""
