from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.properties import Title

from common.value.database_type import DatabaseType


@notion_prop("名前")
class TagTitle(Title):
    pass


@notion_database(DatabaseType.TAG.value)
class Tag(BasePage):
    title: TagTitle
