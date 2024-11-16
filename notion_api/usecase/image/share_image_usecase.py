from dataclasses import dataclass

from common.value.database_type import DatabaseType
from daily_log.infrastructure.daily_log_repository_impl import DailyLogRepositoryImpl
from notion_client_wrapper.block.image import Image
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.page.page_id import PageId
from notion_client_wrapper.properties.cover import Cover
from notion_client_wrapper.properties.title import Title
from util.datetime import jst_today


@dataclass
class ShareImageUrl:
    file: str
    thumbnail: str

    def get_file_name(self) -> str:
        return self.file.split("/")[-1]


@dataclass
class ShareImageRequest:
    images: list[ShareImageUrl]
    additional_page_id: PageId | None = None


class ShareImageUsecase:
    def __init__(
        self,
    ) -> None:
        self._client = ClientWrapper.get_instance()
        self._daily_log_repository = DailyLogRepositoryImpl(client=self._client)

    def execute(
        self,
        request: ShareImageRequest,
    ) -> None:
        if len(request.images) == 0:
            return

        daily_log = self._daily_log_repository.find(date=jst_today(is_previous_day_until_2am=True))

        for photo in request.images:
            image = Image.from_external_url(url=photo.thumbnail, alias_url=photo.file)
            # TODO: 各ドメインのロジックとして実装する

            # デイリーログに追加
            self._client.append_block(
                block_id=daily_log.page_id.value,
                block=image,
            )

            # GIF_JPEGデータベースに追加
            self._client.create_page_in_database(
                database_id=DatabaseType.GIF_JPEG.value,
                properties=[Title.from_plain_text(text=photo.get_file_name())],
                cover=Cover.from_external_url(external_url=photo.thumbnail),
                blocks=[image],
            )

            # 追加で指定されたページに追加
            if request.additional_page_id:
                self._client.append_block(
                    block_id=request.additional_page_id.value,
                    block=image,
                )


if __name__ == "__main__":
    # python -m notion_api.usecase.photo.share_photo_usecase
    request = ShareImageRequest(
        images=[
            ShareImageUrl(
                file="https://d3swar8tu7yuby.cloudfront.net/IMG_3182.JPG",
                thumbnail="https://d3swar8tu7yuby.cloudfront.net/IMG_3182_thumb.JPG",
            ),
        ],
    )
    ShareImageUsecase().execute(request=request)
