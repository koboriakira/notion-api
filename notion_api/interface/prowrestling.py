from typing import Optional
from datetime import date as Date
from custom_logger import get_logger
from usecase.add_prowrestling_usecase import AddProwrestlingUsecase

logger = get_logger(__name__)

def add_page(url: str,
             title: str,
             date: Date,
             promotion: str,
             text: str = "",
             tags: list[str] = [],
             cover: Optional[str] = None,
             ) -> dict:
    logger.debug(f"url: {url}")
    logger.debug(f"title: {title}")
    logger.debug(f"date: {date}")
    logger.debug(f"promotion: {promotion}")
    logger.debug(f"text: {text}")
    logger.debug(f"tags: {tags}")
    logger.debug(f"cover: {cover}")
    usecase = AddProwrestlingUsecase()
    result = usecase.execute(url=url,
                            title=title,
                            date=date,
                            promotion=promotion,
                            text=text,
                            tags=tags,
                            cover=cover,
                            )
    logger.debug(result)
    return result
