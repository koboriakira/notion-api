from fastapi import APIRouter, Header
from typing import Optional
from interface import recipe
from util.access_token import valid_access_token
from router.response.recipe_response import RecipesResponse, Recipe

router = APIRouter()


@router.get("", response_model=RecipesResponse)
def get_recipes(detail_enabled: bool = False,
                access_token: Optional[str] = Header(None),
                ):
    valid_access_token(access_token)
    recipes = recipe.get_recipes(detail_enabled)
    return RecipesResponse(data=[Recipe.from_params(p) for p in recipes])
