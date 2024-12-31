from lotion import notion_database, notion_prop
from lotion.base_page import BasePage
from lotion.properties import Title, Url

from common.value.database_type import DatabaseType


@notion_prop("名前")
class ImageName(Title):
    pass


@notion_prop("URL")
class ImageUrl(Url):
    pass


@notion_database(DatabaseType.GIF_JPEG.value)
class GifJpeg(BasePage):
    title: ImageName
    url: ImageUrl
