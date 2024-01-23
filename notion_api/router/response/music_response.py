from pydantic import Field
from typing import Optional
from router.response.base_response import BaseResponse
from router.response.base_notion_page_model import BaseNotionPageModel
from custom_logger import get_logger

logger = get_logger(__name__)

class Music(BaseNotionPageModel):
    artists: list[str]

    @staticmethod
    def from_params(params: dict) -> "Music":
        logger.debug(f"params:")
        logger.debug(params)
        return Music(
            id=params["id"],
            url=params["url"],
            title=params["title"],
            created_at=params["created_at"],
            updated_at=params["updated_at"],
            artists=params["artists"],
        )
class MusicResponse(BaseResponse):
    data: Optional[Music]

class MusicsResponse(BaseResponse):
    data: list[Music] = Field(default=[])
