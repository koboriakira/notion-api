from dataclasses import dataclass

from lotion.block import Block, BulletedListItem, Heading
from lotion.properties import Cover, Properties, Property

from notion_databases.recipe import (
    Carbohydrate,
    Fat,
    IngredientRelation,
    MealKind,
    Protein,
    Recipe,
    RecipeKind,
    RecipeTitle,
    ReferenceUrl,
)


@dataclass
class RecipeBuilder:
    properties: list[Property]
    blocks: list[Block]
    cover: Cover | None

    @staticmethod
    def of(title: str, blocks: list[Block] | None = None) -> "RecipeBuilder":
        blocks = blocks or []
        properties: list[Property] = [RecipeTitle.from_plain_text(title)]
        return RecipeBuilder(properties=properties, blocks=blocks, cover=None)

    def build(self) -> Recipe:
        return Recipe(properties=Properties(self.properties), block_children=self.blocks, cover=self.cover)

    def add_pfc(self, protein: int, fat: int, carbohydrate: int) -> "RecipeBuilder":
        self.properties.append(Protein.from_num(protein))
        self.properties.append(Fat.from_num(fat))
        self.properties.append(Carbohydrate.from_num(carbohydrate))
        return self

    def add_ingredients(self, ingredient_page_id_list: list[str]) -> "RecipeBuilder":
        self.properties.append(IngredientRelation.from_id_list(ingredient_page_id_list))
        return self

    def add_meal_kind(self, meal_kind: MealKind) -> "RecipeBuilder":
        self.properties.append(meal_kind)
        return self

    def add_recipe_kind(self, recipe_kind: RecipeKind) -> "RecipeBuilder":
        self.properties.append(recipe_kind)
        return self

    def add_reference_url(self, url: str) -> "RecipeBuilder":
        self.properties.append(ReferenceUrl.from_url(url))
        return self

    def add_bulletlist_block(self, heading: str, texts: list[str]) -> "RecipeBuilder":
        heading_block = Heading.from_plain_text(heading_size=2, text=heading)
        self.blocks.append(heading_block)
        items = [BulletedListItem.from_plain_text(text=text) for text in texts]
        self.blocks.extend(items)
        return self
