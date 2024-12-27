from enum import Enum

kind_map = {
    "住居・水道光熱・通信費": {"selected_id": "f3a44bbf-234e-494c-8fdf-3269475da426", "selected_color": "blue"},
    "雑費": {"selected_id": "cd0c84d5-d959-4f06-a929-ec780a7c2d3d", "selected_color": "default"},
    "特別費(東京女子プロレス)": {"selected_id": "19af0797-6750-40e8-a885-1c84d9425803", "selected_color": "green"},
    "趣味・交際費": {"selected_id": "8473f30c-f27c-4fe0-a827-f813c9b9197b", "selected_color": "red"},
    "被服・美容費": {"selected_id": "684dcc6f-ca0b-492b-a9b5-a5096d421a74", "selected_color": "gray"},
    "食費・日用品・生活費": {"selected_id": "5493b7c1-a43d-4f91-89b6-94869393cf85", "selected_color": "purple"},
}


class CategoryType(Enum):
    RESIDENCE_UTILITIES_COMMUNICATIONS = "住居・水道光熱・通信費"
    MISC = "雑費"
    SPECIAL_EXPENSES_TJPW = "特別費(東京女子プロレス)"
    HOBBY_SOCIAL_EXPENSES = "趣味・交際費"
    CLOTHING_BEAUTY_EXPENSES = "被服・美容費"
    FOOD_DAILY_LIVING_EXPENSES = "食費・日用品・生活費"

    @staticmethod
    def from_text(text: str) -> "CategoryType":
        for kind_type in CategoryType:
            if kind_type.value == text:
                return kind_type
        msg = f"CategoryType に存在しない値です: {text}"
        raise ValueError(msg)

    @property
    def priority(self) -> int:
        return {
            CategoryType.TRASH: 0,
            CategoryType.ROUTINE: 1,
            CategoryType.WAIT: 2,
            CategoryType.SOMEDAY_MAYBE: 3,
            CategoryType.SCHEDULE: 4,
            CategoryType.NEXT_ACTION: 5,
            CategoryType.DO_NOW: 6,
        }[self]

    @property
    def selected_name(self) -> str:
        return self.value

    @property
    def selected_id(self) -> str:
        return kind_map[self.value]["selected_id"]

    @property
    def selected_color(self) -> str:
        return kind_map[self.value]["selected_color"]
