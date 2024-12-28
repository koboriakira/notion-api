from lotion import Lotion

from food.domain.food import Food, FoodName


class AddFoodUsecase:
    def __init__(
        self,
        lotion: Lotion,
    ) -> None:
        self._lotion = lotion or Lotion.get_instance()

    def execute(
        self,
        title: str,
    ) -> Food:
        # 情報を取得
        food = self._lotion.find_page(Food, FoodName.from_plain_text(title))
        if food is not None:
            return food

        # ページを生成、保存
        food = Food.generate(title=title)
        return self._lotion.update(food)
