from pydantic import Field

from account_book.domain.account_book import AccountBook as AccountBookEntity
from custom_logger import get_logger
from router.response.base_notion_page_model import BaseNotionPageModel
from router.response.base_response import BaseResponse
from util.datetime import jst_now

logger = get_logger(__name__)


class AccountBook(BaseNotionPageModel):
    @staticmethod
    def from_params(params: dict) -> "AccountBook":
        logger.debug("params:")
        logger.debug(params)
        return AccountBook(
            id=params["id"],
            url=params["url"],
            title=params["title"],
            created_at=params["created_at"],
            updated_at=params["updated_at"],
        )

    @staticmethod
    def from_entity(entity: AccountBookEntity) -> "AccountBook":
        return AccountBook(
            id=entity.id,
            url=entity.url,
            title=entity.get_title_text(),
            created_at=entity.created_time if entity.created_time else jst_now(),
            updated_at=entity.last_edited_time if entity.last_edited_time else jst_now(),
        )


class AccountBookResponse(BaseResponse):
    data: AccountBook | None = None


class AccountBooksResponse(BaseResponse):
    data: list[AccountBook] = Field(default=[])
