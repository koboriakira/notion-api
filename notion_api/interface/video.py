from typing import Optional
from custom_logger import get_logger
from usecase.add_video_usecase import AddVideoUsecase

logger = get_logger(__name__)

def add_page(url: str,
             title: str,
            tags: list[str],
            cover: Optional[str] = None,
            ) -> dict:
    logger.debug(f"url: {url}")
    logger.debug(f"title: {title}")
    logger.debug(f"tags: {tags}")
    logger.debug(f"cover: {cover}")
    usecase = AddVideoUsecase()
    result = usecase.execute(url=url,
                            title=title,
                            tags=tags,
                            cover=cover,
                            )
    logger.debug(result)
    return result
