from typing import override

from lotion.properties import Text


class RoutineOption(Text):
    NAME = "オプション"

    @staticmethod
    @override
    def from_plain_text(text: str) -> "RoutineOption":
        return RoutineOption.from_plain_text(text)
