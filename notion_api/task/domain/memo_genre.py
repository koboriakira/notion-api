from datetime import date, timedelta
from enum import Enum

from common.value.database_type import DatabaseType
from notion_client_wrapper.properties.select import Select

kind_map = {"Webクリップ": {"selected_id": "06f76a53-2354-4911-b15e-7182fb0c845c", "selected_color": "gray"}, "音楽": {"selected_id": "3c4bcf1e-fdb0-4400-a738-e494eb1cdb93", "selected_color": "purple"}, "飲食店": {"selected_id": "17fb8433-e807-415e-9936-e1e912a6b61e", "selected_color": "orange"}, "動画": {"selected_id": "a2155981-a906-47b0-8b52-3dbce2676024", "selected_color": "default"}, "未指定": {"selected_id": "03d9bb99-2d78-4abf-b9bb-7bf772a90524", "selected_color": "yellow"}}


class MemoGenreType(Enum):
    WEBCLIP = "Webクリップ"
    MUSIC = "音楽"
    RESTAURANT = "飲食店"
    VIDEO = "動画"
    UNSPECIFIED = "未指定"

    @property
    def selected_name(self) -> str:
        return self.value

    @property
    def selected_id(self) -> str:
        return kind_map[self.value]["selected_id"]

    @property
    def selected_color(self) -> str:
        return kind_map[self.value]["selected_color"]

    @staticmethod
    def from_text(text: str) -> "MemoGenreType":
        for MemoGenre_type in MemoGenreType:
            if MemoGenre_type.value == text:
                return MemoGenre_type
        msg = f"MemoGenreType not found: {text}"
        raise ValueError(msg)


class MemoGenreKind(Select):
    NAME = "メモジャンル"

    def __init__(self, MemoGenre_type: MemoGenreType) -> None:
        super().__init__(
            name=self.NAME,
            selected_name=MemoGenre_type.selected_name,
            selected_id=MemoGenre_type.selected_id,
            selected_color=MemoGenre_type.selected_color,
            id=None,
        )

    @classmethod
    def create(cls, MemoGenre_type: MemoGenreType) -> "MemoGenreKind":
        return cls(MemoGenre_type=MemoGenre_type)


if __name__ == "__main__":
    # 最新の情報を取得するときに使う
    # python -m notion_api.task.domain.memo_genre
    from util.localonly import get_select

    get_select(database_id=DatabaseType.TASK.value, name=MemoGenreKind.NAME)
