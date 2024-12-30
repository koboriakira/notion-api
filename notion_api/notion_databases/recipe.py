from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.properties import MultiSelect, Number, Relation, Select, Title, Url

from common.value.database_type import DatabaseType


@notion_prop("名前")
class RecipeTitle(Title):
    pass


@notion_prop("状態")
class RecipeKind(Select):
    pass


@notion_prop("種類")
class MealKind(MultiSelect):
    pass


@notion_prop("Ingredients")
class IngredientRelation(Relation):
    pass


@notion_prop("Reference")
class ReferenceUrl(Url):
    pass


@notion_prop("P:タンパク質")
class Protein(Number):
    pass


@notion_prop("F:脂質")
class Fat(Number):
    pass


@notion_prop("C:炭水化物")
class Carbohydrate(Number):
    pass


@notion_database(DatabaseType.RECIPE.value)
class Recipe(BasePage):
    title: RecipeTitle
    recipe_kind: RecipeKind
    meal_kind: MealKind
    ingredients: IngredientRelation
    reference_url: ReferenceUrl
    protein: Protein
    fat: Fat
    carbohydrates: Carbohydrate
