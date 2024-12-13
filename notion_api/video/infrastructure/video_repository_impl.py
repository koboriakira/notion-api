from logging import Logger, getLogger

from lotion import Lotion
from lotion.base_page import BasePage
from lotion.filter import FilterBuilder
from lotion.filter.condition import DateCondition, DateConditionType

from common.value.database_type import DatabaseType
from util.date_range import DateRange
from video.domain.video import Video
from video.domain.video_repository import VideoRepository
from video.domain.video_title import VideoName


class VideoRepositoryImpl(VideoRepository):
    DATABASE_ID = DatabaseType.VIDEO.value

    def __init__(self, client: Lotion, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def search(self, date_range: DateRange) -> list[Video]:
        """Search videos by insert datetime range"""
        filter_builder = FilterBuilder()
        filter_builder = filter_builder.add_condition(
            DateCondition.create_manually(
                name="最終更新日時",
                condition_type=DateConditionType.ON_OR_AFTER,
                value=date_range.start.value,
            ),
        )
        filter_builder = filter_builder.add_condition(
            DateCondition.create_manually(
                name="最終更新日時",
                condition_type=DateConditionType.ON_OR_BEFORE,
                value=date_range.end.value,
            ),
        )
        base_pages = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=filter_builder.build(),
        )
        return [self._cast(base_page) for base_page in base_pages]

    def find_by_title(self, title: str) -> Video | None:
        title_property = VideoName(text=title)
        filter_param = FilterBuilder.build_simple_equal_condition(title_property)
        base_pages = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=filter_param,
        )
        if len(base_pages) == 0:
            return None
        if len(base_pages) > 1:
            warning_message = f"Found multiple video with the same title: {title}"
            self._logger.warning(warning_message)
        return self._cast(base_pages[0])

    def save(self, video: Video) -> Video:
        result = self._client.create_page_in_database(
            database_id=self.DATABASE_ID,
            cover=video.cover,
            properties=video.properties.values,
        )
        video.update_id_and_url(
            page_id=result.page_id.value,
            url=result.url,
        )
        return video

    def _cast(self, base_page: BasePage) -> Video:
        return Video(
            properties=base_page.properties,
            block_children=base_page.block_children,
            id_=base_page.id_,
            url=base_page.url,
            created_time=base_page.created_time,
            last_edited_time=base_page.last_edited_time,
            _created_by=base_page._created_by,
            _last_edited_by=base_page._last_edited_by,
            cover=base_page.cover,
            icon=base_page.icon,
            archived=base_page.archived,
            parent=base_page.parent,
        )
