from shopping.domain.buy_status import BuyStatusType
from shopping.domain.repository import ShoppingRepository


class ResetShoppingListUseCase:
    def __init__(self, shopping_repository: ShoppingRepository) -> None:
        self._shopping_repository = shopping_repository

    def execute(self) -> None:
        all_shopping_list = self._shopping_repository.fetch_all()
        for shopping in all_shopping_list:
            if shopping.buy_status == BuyStatusType.DONE:
                reseted_shopping = shopping.reset_buy_status_type()
                self._shopping_repository.save(reseted_shopping)


if __name__ == "__main__":
    # python -m notion_api.usecase.shopping.reset_shopping_list_usecase
    from notion_client_wrapper.client_wrapper import ClientWrapper
    from shopping.infrastructure.repository_impl import ShoppingRepositoryImpl

    usecase = ResetShoppingListUseCase(
        ShoppingRepositoryImpl(ClientWrapper.get_instance()),
    )
    usecase.execute()
