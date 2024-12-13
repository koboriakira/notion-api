from dataclasses import dataclass

from lotion.base_page import BasePage
from notion_client_wrapper.page.page_id import PageId
from recipe.domain.carbohydrate import Carbohydrate
from recipe.domain.fat import Fat
from recipe.domain.ingredient_relation import IngredientRelation
from recipe.domain.meal_kind import MealKind, MealKindType, MealKindTypes
from recipe.domain.protein import Protein
from recipe.domain.recipe_kind import RecipeKind, RecipeKindType
from recipe.domain.reference_url import ReferenceUrl


@dataclass
class Recipe(BasePage):
    @property
    def carbohydrates(self) -> int | None:
        carbohydrates = self.get_number(name=Carbohydrate.NAME)
        return carbohydrates.number if carbohydrates else None

    @property
    def protein(self) -> int | None:
        protein = self.get_number(name=Protein.NAME)
        return protein.number if protein else None

    @property
    def fat(self) -> int | None:
        fat = self.get_number(name=Fat.NAME)
        return fat.number if fat else None

    @property
    def ingredients(self) -> list[PageId]:
        ingredients = self.get_relation(name=IngredientRelation.NAME)
        return ingredients.page_id_list if ingredients else []

    @property
    def meal_kind(self) -> MealKindTypes:
        meal_kind = self.get_multi_select(name=MealKind.NAME)
        if meal_kind is None:
            return MealKindTypes()
        meal_kind_types = [MealKindType.from_text(el.name) for el in meal_kind.values]
        return MealKindTypes(values=meal_kind_types)

    @property
    def recipe_kind(self) -> RecipeKindType | None:
        recipe_kind = self.get_select(name=RecipeKind.NAME)
        return RecipeKindType.from_text(recipe_kind.selected_name) if recipe_kind else None

    @property
    def reference_url(self) -> str | None:
        url = self.get_url(name=ReferenceUrl.NAME)
        return url.url if url else None
