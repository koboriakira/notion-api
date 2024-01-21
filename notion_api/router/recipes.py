from fastapi import APIRouter, Header
from typing import Optional
from datetime import date as Date
from interface import recipe
from util.access_token import valid_access_token

router = APIRouter()


@router.get("")
def get_recipes(detail_enabled: bool = False,
                access_token: Optional[str] = Header(None),
                ):
    valid_access_token(access_token)
    return recipe.get_recipes(detail_enabled)
