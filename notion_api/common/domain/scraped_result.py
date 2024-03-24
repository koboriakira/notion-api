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
