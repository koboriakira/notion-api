from usecase.recipe_list_usecase import RecipeListUsecase

def get_recipes(detail_enabled: bool = False):
    usecase = RecipeListUsecase()
    return usecase.execute(detail_enabled=detail_enabled)
