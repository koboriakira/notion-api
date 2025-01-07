from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.properties import Title


@notion_prop("名前")
class DreamName(Title):
    pass


@notion_database("1746567a3bbf80da973ee6d98f780a00")
class Dream(BasePage):
    name: DreamName
