from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    not_formatted_text: str
    formatted_text: str
    ogp_tags: dict
    other_meta_tags: dict
