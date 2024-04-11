import re
from dataclasses import dataclass


@dataclass(frozen=True)
class PageId:
    value: str

    def __post_init__(self) -> None:
        # 型チェック
        if not isinstance(self.value, str):
            msg = f"page_idは文字列である必要があります: {self.value}"
            raise TypeError(msg)

        # UUID4の形式であることを確認する
        if not re.match(r"[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}", self.value):
            msg = f"page_idの形式が不正です: {self.value}"
            raise ValueError(msg)

    @staticmethod
    def dummy() -> "PageId":
        return PageId(value="5c38fd30-714b-4ce2-bf2d-25407f3cfc16")
