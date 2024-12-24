from fastapi import APIRouter, Header
from lotion import Lotion
from pydantic import BaseModel

from custom_logger import get_logger
from food.infrastructure.food_repository_impl import FoodRepositoryImpl
from router.response import BaseResponse
from usecase.add_food_usecase import AddFoodUsecase
from util.access_token import valid_access_token

logger = get_logger(__name__)

router = APIRouter()


class AddFoodRequest(BaseModel):
    title: str


@router.post("/")
def add_track_page(request: AddFoodRequest, access_token: str | None = Header(None)) -> BaseResponse:
    valid_access_token(access_token)
    food_repository = FoodRepositoryImpl(client=Lotion.get_instance())
    usecase = AddFoodUsecase(food_repository=food_repository)
    food = usecase.execute(title=request.title)
    return BaseResponse(data={"id": food.id, "url": food.url})
