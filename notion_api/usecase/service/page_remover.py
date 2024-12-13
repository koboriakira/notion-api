from lotion import Lotion
from notion_client_wrapper.page.page_id import PageId


class PageRemover:
    def __init__(self, client: Lotion | None = None) -> None:
        self._client = client or Lotion.get_instance()

    def execute(
        self,
        page_id: PageId,
    ) -> None:
        """指定されたページを削除(アーカイブ)する"""
        self._client.remove_page(page_id=page_id.value)
