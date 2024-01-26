from typing import Optional
from custom_logger import get_logger

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
    pass
    # usecase = AddWebclipUsecase()
    # result = usecase.execute(url=url,
    #                         title=title,
    #                         summary=summary,
    #                         tags=tags,
    #                         status=status,
    #                         cover=cover,
    #                         text=text,
    #                         )
    # logger.debug(result)
    # return result
