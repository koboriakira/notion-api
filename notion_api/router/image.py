from fastapi import APIRouter, Header
from pydantic import BaseModel

from common.domain.external_image import ExternalImage
from custom_logger import get_logger
from router.response import BaseResponse
from usecase.image.share_image_usecase import ShareImageRequest, ShareImageUsecase
from util.access_token import valid_access_token

logger = get_logger(__name__)

router = APIRouter()


class ImageUrl(BaseModel):
    file: str
    thumbnail: str


class ShareImagesRequest(BaseModel):
    images: list[ImageUrl]
    additional_page_id: str | None = None

    def to_usecase_request(self) -> ShareImageRequest:
        return ShareImageRequest(
            images=[ExternalImage(url=i.file, thumbnail_url=i.thumbnail) for i in self.images],
            additional_page_id=self.additional_page_id,
        )


@router.post("/")
def share_images(
    request: ShareImagesRequest,
    access_token: str | None = Header(None),
) -> BaseResponse:
    valid_access_token(access_token)
    usecase = ShareImageUsecase()

    usecase.execute(request=request.to_usecase_request())
    return BaseResponse()
