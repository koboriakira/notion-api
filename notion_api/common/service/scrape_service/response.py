from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    not_formatted_text: str
    formatted_text: str
    ogp_tags: dict
    other_meta_tags: dict

    def get_image_url(self) -> str|None:
        # 他にあればもっと付け足す
        return self.ogp_tags.get("image") or self.other_meta_tags.get("image")
