from logging import Logger, getLogger

from common.value.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from recipe.domain.recipe import Recipe
from recipe.domain.recipe_repository import RecipeRepository


class RecipeRepositoryImpl(RecipeRepository):
    DATABASE_ID = DatabaseType.RECIPE.value

    def __init__(self, client: ClientWrapper, logger: Logger | None = None) -> None:
        self._client = client
        self._logger = logger or getLogger(__name__)

    def save(self, recipe: Recipe) -> Recipe:
        result = self._client.create_page_in_database(
            database_id=self.DATABASE_ID,
            cover=recipe.cover,
            properties=recipe.properties.values,
            blocks=recipe.block_children,
        )
        recipe.update_id_and_url(
            page_id=result["id"],
            url=result["url"],
        )
        return recipe
