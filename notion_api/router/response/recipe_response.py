from pydantic import Field
from typing import Optional
from router.response.base_response import BaseResponse
from router.response.base_notion_page_model import BaseNotionPageModel
from custom_logger import get_logger

logger = get_logger(__name__)

class Recipe(BaseNotionPageModel):
    ingredients: list[str]
    meal_categories: list[str]
    status: str

    @staticmethod
    def from_params(params: dict) -> "Recipe":
        logger.debug(f"params:")
        logger.debug(params)
        return Recipe(
            id=params["id"],
            url=params["url"],
            title=params["title"],
            created_at=params["created_at"],
            updated_at=params["updated_at"],
            ingredients=params["ingredients"],
            meal_categories=params["meal_categories"],
            status=params["status"],
        )

class RecipeResponse(BaseResponse):
    data: Optional[Recipe]

class RecipesResponse(BaseResponse):
    data: list[Recipe] = Field(default=[])
