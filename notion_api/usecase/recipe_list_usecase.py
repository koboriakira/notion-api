from common.value.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper


class RecipeListUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()

    def execute(
        self,
        detail_enabled: bool = False,
    ):
        # 食材マスタ
        ingredient_list = self.client.retrieve_database(database_id=DatabaseType.INGREDIENTS.value)
        ingredients_map = {}
        for ingredient in ingredient_list:
            title = ingredient.get_title()
            ingredients_map[ingredient.id] = title.text

        # まずレシピを検索する
        searched_recipes = self.client.retrieve_database(database_id=DatabaseType.RECIPE.value)
        recipes = []
        for recipe in searched_recipes:
            title = recipe.get_title()
            ingredients_relation = recipe.get_relation(name="Ingredients")
            ingredients = [ingredients_map[id] for id in ingredients_relation.id_list]
            meal_categories = recipe.get_multi_select(name="種類")
            daily_log_relation = recipe.get_relation(name="デイリーログ")
            select = recipe.get_select(name="状態")

            recipes.append(
                {
                    "id": recipe.id,
                    "url": recipe.url,
                    "title": title.text,
                    "updated_at": recipe.last_edited_time.start_time,
                    "created_at": recipe.created_time.start_time,
                    "daily_log_id": daily_log_relation.id_list,
                    "ingredients": ingredients,
                    "meal_categories": [c.name for c in meal_categories.values] if meal_categories is not None else [],
                    "status": select.selected_name if select is not None else "",
                }
            )
        if detail_enabled:
            # ヒットしたレシピの詳細を取得する
            pass
        return recipes
