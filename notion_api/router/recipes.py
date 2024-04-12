from fastapi import APIRouter, Header

from interface import recipe
from router.response.recipe_response import Recipe, RecipesResponse
from util.access_token import valid_access_token

router = APIRouter()


@router.get("", response_model=RecipesResponse)
def get_recipes(
    detail_enabled: bool | None = None,
    access_token: str | None = Header(None),
) -> RecipesResponse:
    valid_access_token(access_token)
    recipes = recipe.get_recipes(detail_enabled or False)
    return RecipesResponse(data=[Recipe.from_params(p) for p in recipes])
