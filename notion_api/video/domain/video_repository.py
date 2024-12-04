from abc import ABCMeta, abstractmethod

from common.value.database_type import DatabaseType
from util.date_range import DateRange
from video.domain.video import Video


class VideoRepository(metaclass=ABCMeta):
    DATABASE_ID = DatabaseType.VIDEO.value

    @abstractmethod
    def search(self, insert_datetime_range: DateRange) -> list[Video]:
        """Search videos by insert datetime range"""

    @abstractmethod
    def find_by_title(self, title: str) -> Video | None:
        """Find a video by title"""

    @abstractmethod
    def save(self, video: Video) -> Video:
        """Save a video"""
