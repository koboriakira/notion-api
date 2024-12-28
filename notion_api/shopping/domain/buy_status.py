from enum import Enum


class BuyStatusType(Enum):
    """
    タスクのステータス
    """

    UNDONE = "未購入"
    DONE = "購入済"

    @staticmethod
    def from_text(text: str) -> "BuyStatusType":
        for status_type in BuyStatusType:
            if status_type.value.lower() == text.lower():
                return status_type
        msg = f"BuyStatusType に存在しない値です: {text}"
        raise ValueError(msg)

    @staticmethod
    def get_status_list(status_list: list[str] | None) -> list["BuyStatusType"]:
        if status_list is None:
            return []
        return [BuyStatusType.from_text(status) for status in status_list]

    def is_done(self) -> bool:
        return self == BuyStatusType.DONE

    def is_undone(self) -> bool:
        return self == BuyStatusType.UNDONE
