from logging import Logger, getLogger

from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from video.domain.video import Video
from video.domain.video_title import VideoName


class VideoRepositoryImpl:
    DATABASE_ID = DatabaseType.VIDEO.value

    def __init__(
            self,
            client: ClientWrapper,
            logger: Logger|None = None) -> None :
        self._client = client
        self._logger = logger or getLogger(__name__)

    def find_by_title(self, title: str) -> Video|None:
        title_property = VideoName(text=title)
        filter_param = FilterBuilder.build_simple_equal_condition(title_property)
        searched_video = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=filter_param,
            page_model=Video,
        )
        if len(searched_video) == 0:
            return None
        if len(searched_video) > 1:
            warning_message = f"Found multiple video with the same title: {title}"
            self._logger.warning(warning_message)
        return searched_video[0]

    def save(self, video: Video) -> Video:
        result = self._client.create_page_in_database(
            database_id=self.DATABASE_ID,
            cover=video.cover,
            properties=video.properties.values,
        )
        video.update_id_and_url(
            page_id=result["id"],
            url=result["url"],
        )
        return video
