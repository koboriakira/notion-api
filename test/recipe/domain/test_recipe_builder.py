from unittest import TestCase

from recipe.domain.meal_kind import MealKindType, MealKindTypes
from recipe.domain.recipe_builder import RecipeBuilder
from recipe.domain.recipe_kind import RecipeKindType


class TestRecipeBuilder(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test(self):
        # Given
        meal_kinds = MealKindTypes(values=[MealKindType.SIDE_DISH])
        recipe_kind = RecipeKindType.YET

        # When
        recipe = (
            RecipeBuilder.of(title="ブロッコリーチーズガレット")
            .add_reference_url(url="https://twitter.com/dietmenuplan/status/1690241946542030848")
            .add_recipe_kind(recipe_kind)
            .add_meal_kind(meal_kinds)
            .add_pfc(protein=10, fat=20, carbohydrate=30)
            .build()
        )

        # Then
        self.assertEqual(recipe.get_title_text(), "ブロッコリーチーズガレット")
        self.assertEqual(recipe.reference_url, "https://twitter.com/dietmenuplan/status/1690241946542030848")
        self.assertEqual(recipe.recipe_kind, recipe_kind)
        self.assertEqual(recipe.meal_kind, meal_kinds)
        self.assertEqual(recipe.protein, 10)
        self.assertEqual(recipe.fat, 20)
        self.assertEqual(recipe.carbohydrates, 30)
