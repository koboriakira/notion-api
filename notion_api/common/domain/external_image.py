from dataclasses import dataclass

from lotion.block import Image


@dataclass
class ExternalImage:
    url: str
    thumbnail_url: str | None = None
    title: str | None = None

    def get_title(self) -> str:
        return self.title if self.title else self.url.split("/")[-1]

    def to_notion_image_block(self, use_thumbnail: bool | None = None) -> Image:
        if use_thumbnail and self.thumbnail_url:
            return Image.from_external_url(url=self.thumbnail_url, alias_url=self.url)
        return Image.from_external_url(url=self.url)
