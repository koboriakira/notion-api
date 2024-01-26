from typing import Optional
from usecase.add_webclip_usecase import AddWebclipUsecase
from custom_logger import get_logger

logger = get_logger(__name__)

def add_page(url: str,
             title: str,
            summary: str,
            tags: list[str],
            status: str = "Inbox",
            cover: Optional[str] = None,
            text: Optional[str] = None,
            ) -> dict:
    logger.debug(f"url: {url}")
    logger.debug(f"title: {title}")
    logger.debug(f"summary: {summary}")
    logger.debug(f"tags: {tags}")
    logger.debug(f"cover: {cover}")
    logger.debug(f"status: {status}")
    logger.debug(f"text: {text}")

    usecase = AddWebclipUsecase()
    result = usecase.execute(url=url,
                            title=title,
                            summary=summary,
                            tags=tags,
                            status=status,
                            cover=cover,
                            text=text,
                            )
    logger.debug(result)
    return result
