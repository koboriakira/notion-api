from enum import Enum


class AccountTag(Enum):
    MUSIC_BAR_T = "music bar t"

    @staticmethod
    def from_text(text: str) -> "AccountTag":
        for kind_type in AccountTag:
            if kind_type.value == text:
                return kind_type
        msg = f"AccountTag に存在しない値です: {text}"
        raise ValueError(msg)
