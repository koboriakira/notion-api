from dataclasses import dataclass

from lotion import Lotion

from common.domain.external_image import ExternalImage
from common.service.image.external_image_service import ExternalImageService
from daily_log.daily_log_repository_impl import DailyLogRepositoryImpl
from util.datetime import jst_today


@dataclass
class ShareImageRequest:
    images: list[ExternalImage]
    additional_page_id: str | None = None


class ShareImageUsecase:
    def __init__(
        self,
        client: Lotion | None = None,
    ) -> None:
        self._client = client or Lotion.get_instance()
        self._image_service = ExternalImageService(client=self._client)
        self._daily_log_repository = DailyLogRepositoryImpl(client=self._client)

    def execute(
        self,
        request: ShareImageRequest,
    ) -> None:
        if len(request.images) == 0:
            return

        daily_log = self._daily_log_repository.find(date=jst_today(is_previous_day_until_2am=True))

        for image in request.images:
            # GIF_JPEGデータベースに追加
            _ = self._image_service.add_external_image(external_image=image)

            # デイリーログに追加
            self._client.append_block(
                block_id=daily_log.page_id.value,  # type: ignore
                block=image.to_notion_image_block(use_thumbnail=True),
            )

            # 追加で指定されたページに追加
            if request.additional_page_id:
                self._client.append_block(
                    block_id=request.additional_page_id,
                    block=image.to_notion_image_block(use_thumbnail=True),
                )


if __name__ == "__main__":
    # python -m notion_api.usecase.image.share_image_usecase
    request = ShareImageRequest(
        images=[
            ExternalImage(
                url="https://d3swar8tu7yuby.cloudfront.net/IMG_3182.JPG",
                thumbnail_url="https://d3swar8tu7yuby.cloudfront.net/IMG_3182_thumb.JPG",
            ),
        ],
    )
    ShareImageUsecase().execute(request=request)
