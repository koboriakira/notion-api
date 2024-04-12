from dataclasses import dataclass

from notion_client_wrapper.block.block import Block
from notion_client_wrapper.page.page_id import PageId
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.properties import Properties
from notion_client_wrapper.properties.property import Property
from notion_client_wrapper.properties.title import Title
from recipe.domain.carbohydrate import Carbohydrate
from recipe.domain.fat import Fat
from recipe.domain.ingredient_relation import IngredientRelation
from recipe.domain.meal_kind import MealKind, MealKindTypes
from recipe.domain.protein import Protein
from recipe.domain.recipe import Recipe
from recipe.domain.recipe_kind import RecipeKind, RecipeKindType
from recipe.domain.reference_url import ReferenceUrl


@dataclass
class RecipeBuilder:
    properties: list[Property]
    blocks: list[Block]
    cover: Cover | None

    @staticmethod
    def of(title: str, blocks: list[Block] | None = None) -> "RecipeBuilder":
        blocks = blocks or []
        properties = [Title.from_plain_text(text=title)]
        return RecipeBuilder(properties=properties, blocks=blocks, cover=None)

    def build(self) -> Recipe:
        return Recipe(properties=Properties(self.properties), block_children=self.blocks, cover=self.cover)

    def add_pfc(self, protein: int, fat: int, carbohydrate: int) -> "RecipeBuilder":
        self.properties.append(Protein(number=protein))
        self.properties.append(Fat(number=fat))
        self.properties.append(Carbohydrate(number=carbohydrate))
        return self

    def add_ingredients(self, ingredient_page_id_list: list[PageId]) -> "RecipeBuilder":
        self.properties.append(IngredientRelation.from_id_list(id_list=ingredient_page_id_list))
        return self

    def add_meal_kind(self, meal_kind_types: MealKindTypes) -> "RecipeBuilder":
        self.properties.append(MealKind(kind_types=meal_kind_types))
        return self

    def add_recipe_kind(self, recipe_kind_type: RecipeKindType) -> "RecipeBuilder":
        self.properties.append(RecipeKind(kind_type=recipe_kind_type))
        return self

    def add_reference_url(self, url: str) -> "RecipeBuilder":
        self.properties.append(ReferenceUrl(url=url))
        return self
