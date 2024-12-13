from dataclasses import dataclass

from notion_client_wrapper.block.block import Block
from notion_client_wrapper.block.bulleted_list_item import BulletedlistItem
from notion_client_wrapper.block.heading import Heading
from lotion.page import PageId
from lotion.properties import Cover
from lotion.properties import Properties
from lotion.properties import Property
from recipe.domain.carbohydrate import Carbohydrate
from recipe.domain.fat import Fat
from recipe.domain.ingredient_relation import IngredientRelation
from recipe.domain.meal_kind import MealKind, MealKindTypes
from recipe.domain.protein import Protein
from recipe.domain.recipe import Recipe
from recipe.domain.recipe_kind import RecipeKind, RecipeKindType
from recipe.domain.recipe_title import RecipeTitle
from recipe.domain.reference_url import ReferenceUrl


@dataclass
class RecipeBuilder:
    properties: list[Property]
    blocks: list[Block]
    cover: Cover | None

    @staticmethod
    def of(title: str, blocks: list[Block] | None = None) -> "RecipeBuilder":
        blocks = blocks or []
        properties = [RecipeTitle(text=title)]
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
        meal_kind = MealKind(kind_types=meal_kind_types)
        print(meal_kind)
        self.properties.append(meal_kind)
        return self

    def add_recipe_kind(self, recipe_kind_type: RecipeKindType) -> "RecipeBuilder":
        self.properties.append(RecipeKind(kind_type=recipe_kind_type))
        return self

    def add_reference_url(self, url: str) -> "RecipeBuilder":
        self.properties.append(ReferenceUrl(url=url))
        return self

    def add_bulletlist_block(self, heading: str, texts: list[str]) -> "RecipeBuilder":
        heading_block = Heading.from_plain_text(heading_size=2, text=heading)
        self.blocks.append(heading_block)
        items = [BulletedlistItem.from_plain_text(text=text) for text in texts]
        self.blocks.extend(items)
        return self
