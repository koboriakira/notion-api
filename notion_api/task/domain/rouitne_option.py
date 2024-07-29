from typing import override

from notion_client_wrapper.properties.text import Text


class RoutineOption(Text):
    NAME = "オプション"

    @staticmethod
    @override
    def from_plain_text(text: str) -> "RoutineOption":
        return RoutineOption.from_plain_text(text)
