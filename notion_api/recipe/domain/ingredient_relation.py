from lotion.properties import Relation


class IngredientRelation(Relation):
    NAME = "Ingredients"

    def __init__(self, id_list: list[str]) -> None:
        super().__init__(
            name=self.NAME,
            id_list=id_list,
        )

    @staticmethod
    def empty() -> "IngredientRelation":
        return IngredientRelation(id_list=[])

    @staticmethod
    def from_id_list(id_list: list[str]) -> "IngredientRelation":
        return IngredientRelation(id_list=id_list)

    def add(self, page_id: str) -> "IngredientRelation":
        return IngredientRelation(id_list=[*self.id_list, page_id])
