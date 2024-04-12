from fastapi import APIRouter, Header

from injector.injector import Injector
from interface import recipe
from router.request.recipe_request import AddRecipeRequest
from router.response.recipe_response import Recipe, RecipeResponse, RecipesResponse
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


@router.post("", response_model=RecipeResponse)
def add(
    request: AddRecipeRequest,
    access_token: str | None = Header(None),
) -> RecipeResponse:
    valid_access_token(access_token)
    usecase = Injector.create_add_recipe_use_case()
    recipe = usecase.execute(
        description=request.description,
        reference_url=request.reference_url,
    )
    return RecipeResponse(data=Recipe.from_entity(entity=recipe))
