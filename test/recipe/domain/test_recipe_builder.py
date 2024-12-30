from unittest import TestCase

from recipe.domain.meal_kind import MealKindType, MealKindTypes
from recipe.domain.recipe import MealKind, RecipeKind
from recipe.domain.recipe_builder import RecipeBuilder
from recipe.domain.recipe_kind import RecipeKindType


class TestRecipeBuilder(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test(self):
        # Given
        meal_kind_types = MealKindTypes(values=[MealKindType.SIDE_DISH])
        recipe_kind_type = RecipeKindType.YET
        meal_kind = MealKind.from_name(meal_kind_types.to_str_list())
        recipe_kind = RecipeKind.from_name(recipe_kind_type.value)

        # When
        recipe = (
            RecipeBuilder.of(title="ブロッコリーチーズガレット")
            .add_reference_url(url="https://twitter.com/dietmenuplan/status/1690241946542030848")
            .add_recipe_kind(recipe_kind)
            .add_meal_kind(meal_kind)
            .add_pfc(protein=10, fat=20, carbohydrate=30)
            .build()
        )

        # Then
        self.assertEqual(recipe.get_title_text(), "ブロッコリーチーズガレット")
        self.assertEqual(recipe.reference_url.url, "https://twitter.com/dietmenuplan/status/1690241946542030848")
        self.assertEqual(recipe.recipe_kind.selected_name, recipe_kind_type.value)
        self.assertEqual(len(recipe.meal_kind.values), len(meal_kind_types.values))
        self.assertEqual(recipe.protein.number, 10)
        self.assertEqual(recipe.fat.number, 20)
        self.assertEqual(recipe.carbohydrates.number, 30)
