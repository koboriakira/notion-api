from logging import Logger, getLogger

from lotion import Lotion

from notion_databases.shopping import Shopping


class ResetShoppingListUseCase:
    def __init__(self, lotion: Lotion | None = None, logger: Logger | None = None) -> None:
        self._lotion = lotion or Lotion.get_instance()
        self._logger = logger or getLogger(__name__)

    def execute(self) -> None:
        all_shopping_list = self._lotion.retrieve_pages(Shopping)
        for shopping in all_shopping_list:
            if shopping.is_bought():
                self._logger.info(f"Reset buy status: {shopping.name.text}")
                reseted_shopping = shopping.reset_buy_status_type()
                self._lotion.update(reseted_shopping)


if __name__ == "__main__":
    # python -m notion_api.usecase.shopping.reset_shopping_list_usecase
    from lotion import Lotion

    usecase = ResetShoppingListUseCase()
    usecase.execute()
