from typing import Optional
from custom_logger import get_logger
from usecase.add_video_usecase import AddVideoUsecase

logger = get_logger(__name__)

def add_page(
        url: str,
        title: str,
        tags: list[str],
        cover: Optional[str] = None,
        slack_channel: Optional[str] = None,
        slack_thread_ts: Optional[str] = None,
            ) -> dict:
    logger.debug(f"url: {url}")
    logger.debug(f"title: {title}")
    logger.debug(f"tags: {tags}")
    logger.debug(f"cover: {cover}")
    logger.debug(f"slack_channel: {slack_channel}")
    logger.debug(f"slack_thread_ts: {slack_thread_ts}")

    usecase = AddVideoUsecase()
    result = usecase.execute(
        url=url,
        title=title,
        tags=tags,
        cover=cover,
        slack_channel=slack_channel,
        slack_thread_ts=slack_thread_ts,
        )
    logger.debug(result)
    return result
