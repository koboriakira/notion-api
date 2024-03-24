from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    def __init__(
            self,
            not_formatted_text: str,
            formatted_text: str,
            ogp_tags: dict,
            other_meta_tags: dict) -> None:
        self.not_formatted_text = not_formatted_text
        self.formatted_text = formatted_text
        self.ogp_tags = ogp_tags
        self.other_meta_tags = other_meta_tags
