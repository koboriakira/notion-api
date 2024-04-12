from pydantic import Field

from custom_logger import get_logger
from recipe.domain.recipe import Recipe as RecipeEntity
from router.response.base_notion_page_model import BaseNotionPageModel
from router.response.base_response import BaseResponse

logger = get_logger(__name__)


class Recipe(BaseNotionPageModel):
    @staticmethod
    def from_params(params: dict) -> "Recipe":
        logger.debug("params:")
        logger.debug(params)
        return Recipe(
            id=params["id"],
            url=params["url"],
            title=params["title"],
            created_at=params["created_at"],
            updated_at=params["updated_at"],
        )

    @staticmethod
    def from_entity(entity: RecipeEntity) -> "Recipe":
        return Recipe(
            id=entity.id,
            url=entity.url,
            title=entity.title,
            created_at=entity.created_time.start_datetime,
            updated_at=entity.last_edited_time.start_datetime,
        )


class RecipeResponse(BaseResponse):
    data: Recipe | None


class RecipesResponse(BaseResponse):
    data: list[Recipe] = Field(default=[])
