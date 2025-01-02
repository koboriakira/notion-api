from lotion import notion_prop
from lotion.properties import Title


@notion_prop("名前")
class ProjectName(Title):
    pass
