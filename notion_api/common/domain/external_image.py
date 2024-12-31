from dataclasses import dataclass

from lotion.block import Image
from lotion.properties.cover import Cover

from notion_databases.external_image import GifJpeg, ImageName, ImageUrl


@dataclass
class ExternalImage:
    url: str
    thumbnail_url: str | None = None
    title: str | None = None

    def get_title(self) -> str:
        return self.title if self.title else self.url.split("/")[-1]

    def to_gif_jpeg_page(self, use_thumbnail: bool | None = None) -> GifJpeg:
        image_block = self.to_notion_image_block(use_thumbnail)
        cover = self._to_cover()

        return GifJpeg.create(
            [
                ImageName.from_plain_text(self.get_title()),
                ImageUrl.from_url(self.url),
            ],
            [image_block],
            cover,
        )

    def to_notion_image_block(self, use_thumbnail: bool | None = None) -> Image:
        if use_thumbnail and self.thumbnail_url:
            return Image.from_external_url(url=self.thumbnail_url, alias_url=self.url)
        return Image.from_external_url(url=self.url)

    def _to_cover(self) -> Cover | None:
        return Cover.from_external_url(self.thumbnail_url) if self.thumbnail_url else None
