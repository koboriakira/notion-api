from lotion import Lotion


class PageRemover:
    def __init__(self, client: Lotion | None = None) -> None:
        self._client = client or Lotion.get_instance()

    def execute(
        self,
        page_id: str,
    ) -> None:
        """指定されたページを削除(アーカイブ)する"""
        self._client.remove_page(page_id=page_id)
