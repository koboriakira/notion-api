from common.domain.external_image import ExternalImage
from common.value.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.page.page_id import PageId
from notion_client_wrapper.properties import Title
from notion_client_wrapper.properties.cover import Cover


class ExternalImageService:
    DATABASE_ID = DatabaseType.GIF_JPEG.value

    def __init__(self, client: ClientWrapper | None = None) -> None:
        self._client = client or ClientWrapper.get_instance()

    def add_external_image(self, external_image: ExternalImage) -> PageId:
        """指定された画像をGIF/JPEGデータベースに追加する。画像ページのIDを返却する。"""
        image = external_image.to_notion_image_block(use_thumbnail=True)
        page_dict = self._client.create_page_in_database(
            database_id=self.DATABASE_ID,
            properties=[Title.from_plain_text(text=external_image.get_title())],
            cover=Cover.from_external_url(external_url=external_image.thumbnail_url),
            blocks=[image],
        )
        return PageId(page_dict["id"])
