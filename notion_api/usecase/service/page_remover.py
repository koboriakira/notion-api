from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.page.page_id import PageId


class PageRemover:
    def __init__(self, client: ClientWrapper | None = None) -> None:
        self._client = client or ClientWrapper.get_instance()

    def execute(
        self,
        page_id: PageId,
    ) -> None:
        """指定されたページを削除(アーカイブ)する"""
        self._client.remove_page(page_id=page_id.value)
