from abc import ABCMeta, abstractmethod

from recipe.domain.recipe import Recipe


class RecipeRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, recipe: Recipe) -> Recipe:
        pass
