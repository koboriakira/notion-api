from typing import override

from notion_client_wrapper.properties.text import Text


class RoutineTime(Text):
    NAME = "時間"

    @classmethod
    @override
    def from_plain_text(cls, text: str) -> "RoutineTime":
        return cls.from_plain_text(text)
