import re
from dataclasses import dataclass


@dataclass(frozen=True)
class PageId:
    value: str

    def __post_init__(self) -> None:
        # 5c38fd30714b4ce2bf2d25407f3cfc16
        # 5c38fd30-714b-4ce2-bf2d-25407f3cfc16
        # どちらかの形式であることを確認する
        if not re.match(r"[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}", self.value):
            msg = f"page_idの形式が不正です: {self.value}"
            raise ValueError(msg)
