from typing import Optional
from usecase.add_webclip_usecase import AddWebclipUsecase
from custom_logger import get_logger

logger = get_logger(__name__)

def add_page(
        url: str,
        title: str,
        cover: Optional[str] = None,
        slack_channel: Optional[str] = None,
        slack_thread_ts: Optional[str] = None,
        ) -> dict:
        logger.debug(f"url: {url}")
        logger.debug(f"title: {title}")
        logger.debug(f"cover: {cover}")
        logger.debug(f"slack_channel: {slack_channel}")
        logger.debug(f"slack_thread_ts: {slack_thread_ts}")

        usecase = AddWebclipUsecase()
        result = usecase.execute(
                url=url,
                title=title,
                cover=cover,
                slack_channel=slack_channel,
                slack_thread_ts=slack_thread_ts,
                )
        logger.debug(result)
        return result
