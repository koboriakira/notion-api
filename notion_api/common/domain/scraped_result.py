from dataclasses import dataclass


class ScrapeError(Exception):
    pass

@dataclass(frozen=True)
class OgpTags:
    values: dict

@dataclass(frozen=True)
class OtherMetaTags:
    values: dict

@dataclass(frozen=True)
class ScrapedResult:
    not_formatted_text: str
    formatted_text: str
    ogp_tags: OgpTags
    other_meta_tags: OtherMetaTags

    def get_image_url(self) -> str|None:
        """画像URLを見つける"""
        # 他にあればもっと付け足す
        return self.ogp_tags.values.get("image") or self.other_meta_tags.values.get("image")
