from food.domain.food import Food
from food.domain.food_repository import FoodRepository


class AddFoodUsecase:
    def __init__(
        self,
        food_repository: FoodRepository,
    ) -> None:
        self._food_repository = food_repository

    def execute(
        self,
        title: str,
    ) -> Food:
        # 情報を取得
        food = self._food_repository.find_by_title(title=title)
        if food is not None:
            return food

        # ページを生成、保存
        food = Food.create(title=title)
        return self._food_repository.save(food=food)
