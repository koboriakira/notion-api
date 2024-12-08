from enum import Enum


class DatabaseType(Enum):
    """
    各データベースのID
    """

    DAILY_LOG = "58da568b-4e63-4a46-9ffe-36adeb59ab30"
    MUSIC = "ef2d1550-3edb-4848-b236-229fb83d31e0"
    TAG = "8356ec79-ce5f-4aea-bad2-c8dc49098885"
    HABIT_TRACKER_ALLDAY = "752e93c9-9a9c-4bef-8d1f-7702439f658a"
    HABIT_TRACKER_MORNING = "df0ee11c-90a8-46d5-b8bf-aac52f8d8bcd"
    HABIT_TRACKER_NIGHT = "a759f224-ebb8-40c0-9047-6d7f88835e65"
    INGREDIENTS = "dba77be1-c1a6-40a2-858e-85878ee55b0d"
    WEEKLY_LOG = "3ae412cf-6c87-4119-a9c6-ffdb2eee2a1e"
    PROJECT = "458c69ce-4e1c-49fe-810c-f26c2291e294"
    PROJECT_BK = "1436567a-3bbf-8020-9d12-d71654dd9f6d"
    ZETTLEKASTEN = "2dd39a65-3f14-45e1-a51e-2c3d857a8321"
    RECIPE = "64b6d5f1-2547-41a2-a74d-25f0c4df041e"
    PROWRESTLING = "2816de0d-9a02-4289-85c1-f54b2a14064a"
    BOOK = "cbe1dc60-5cb7-4c4a-9519-0accaea737df"
    WEBCLIP = "b5e701d7-75d0-4355-8c59-dc3e2f0c09ac"
    MONTHLY_LOG = "043ecb87-268c-48d8-93e7-18702808b3be"
    VIDEO = "e84f3d8b-7cf3-4e3c-b55e-7ff251064149"
    TASK = "3b97e3ba-a84e-40a9-bdc8-99ee25d8e99d"
    TASK_BK = "26594969-6394-41d8-b4bd-88ed801a2bdd"
    TASK_ROUTINE = "d21db86c-9203-4ff4-9899-9d62354e8fe1"
    RESTAURANT = "4f10b337-9a1d-4b87-9feb-87a00c511b68"
    GOAL = "f3f8b93f-d89f-4c3d-a47a-01c134a7e2bf"
    GOAL_BK = "1566567a-3bbf-80a4-a079-dcba0e1bf9f9"
    SHOPPING = "b917fd7e-2fe5-4030-879f-9eea5e8827bb"
    ACCOUNT_BOOK = "f2c5fc6e-4c27-429f-add5-2279f1f84e8d"
    GIF_JPEG = "1156567a-3bbf-808f-ae6f-cf20cbba8f28"

    @staticmethod
    def from_id(id_: str) -> "DatabaseType":
        """
        IDからデータベースの種類を取得する
        """
        for database_type in DatabaseType:
            if database_type.value.replace("-", "") == id_.replace("-", ""):
                return database_type
        msg = f"ID={id_}に対忋するデータベースが見つかりませんでした"
        raise ValueError(msg)

    def title_name(self) -> str:
        return "名前"

    def name_last_edited_time(self) -> str:
        """
        更新日時のプロパティ名を返す
        """
        match self:
            case _:
                return "最終更新日時"

    def name_created_time(self) -> str:
        """
        作成日時のプロパティ名を返す
        """
        match self:
            case _:
                return "作成日時"

    @staticmethod
    def ignore_updated_at() -> list[str]:
        """
        更新日時を無視するデータベースのIDを返す
        """
        return [
            DatabaseType.DAILY_LOG.value,
            DatabaseType.TAG.value,
            DatabaseType.HABIT_TRACKER_ALLDAY.value,
            DatabaseType.HABIT_TRACKER_MORNING.value,
            DatabaseType.HABIT_TRACKER_NIGHT.value,
            DatabaseType.INGREDIENTS.value,
        ]
