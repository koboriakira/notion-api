from common.domain.external_image import ExternalImage
from common.value.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.condition.date_condition import DateCondition, DateConditionType
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_client_wrapper.page.page_id import PageId
from notion_client_wrapper.properties import Title
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.url import Url
from util.date_range import DateRange


class ExternalImageService:
    DATABASE_ID = DatabaseType.GIF_JPEG.value

    def __init__(self, client: ClientWrapper | None = None) -> None:
        self._client = client or ClientWrapper.get_instance()

    def add_external_image(self, external_image: ExternalImage) -> PageId:
        """指定された画像をGIF/JPEGデータベースに追加する。画像ページのIDを返却する。"""
        image = external_image.to_notion_image_block(use_thumbnail=True)
        page_dict = self._client.create_page_in_database(
            database_id=self.DATABASE_ID,
            properties=[
                Title.from_plain_text(text=external_image.get_title()),
                Url.from_url(url=external_image.url),
            ],
            cover=Cover.from_external_url(external_url=external_image.thumbnail_url),
            blocks=[image],
        )
        return PageId(page_dict["id"])

    def append_image(self, block_id: str, external_image: ExternalImage) -> None:
        """指定された画像を指定されたブロックに追加する。"""
        image = external_image.to_notion_image_block(use_thumbnail=True)
        self._client.append_block(block_id=block_id, block=image)

    def get_images(self, date_range: DateRange) -> list[str]:
        """GIF/JPEGデータベースに登録されている画像の(サムネイル)URLを取得する。"""
        filter_builder = FilterBuilder()
        filter_builder = filter_builder.add_condition(
            DateCondition.create_manually(
                name="作成日時",
                condition_type=DateConditionType.ON_OR_AFTER,
                value=date_range.start.value,
            ),
        )
        filter_builder = filter_builder.add_condition(
            DateCondition.create_manually(
                name="作成日時",
                condition_type=DateConditionType.ON_OR_BEFORE,
                value=date_range.end.value,
            ),
        )
        base_pages = self._client.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=filter_builder.build(),
        )
        return [base_page.get_url(name="URL").url for base_page in base_pages]
