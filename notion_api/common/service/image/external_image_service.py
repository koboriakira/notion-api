from lotion import Lotion

from common.domain.external_image import ExternalImage
from common.value.database_type import DatabaseType
from notion_databases.external_image import GifJpeg
from util.date_range import DateRange


class ExternalImageService:
    DATABASE_ID = DatabaseType.GIF_JPEG.value

    def __init__(self, client: Lotion | None = None) -> None:
        self._client = client or Lotion.get_instance()

    def add_external_image(self, external_image: ExternalImage) -> GifJpeg:
        """指定された画像をGIF/JPEGデータベースに追加する。画像ページのIDを返却する。"""
        gif_jpeg_page = external_image.to_gif_jpeg_page(use_thumbnail=True)
        return self._client.update(gif_jpeg_page)

    def append_image(self, block_id: str, external_image: ExternalImage) -> None:
        """指定された画像を指定されたブロックに追加する。"""
        image = external_image.to_notion_image_block(use_thumbnail=True)
        self._client.append_block(block_id=block_id, block=image)

    def get_images(self, date_range: DateRange) -> list[str]:
        """GIF/JPEGデータベースに登録されている画像の(サムネイル)URLを取得する。"""

        gif_jpeg_pages = self._client.search_page_by_created_at(
            GifJpeg,
            date_range.start.value,
            date_range.end.value,
        )
        return [page.url.url for page in gif_jpeg_pages]
