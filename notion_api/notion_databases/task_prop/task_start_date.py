from lotion import notion_prop
from lotion.properties import Date


@notion_prop("実施日")
class TaskStartDate(Date):
    pass
