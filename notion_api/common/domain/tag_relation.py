from lotion import notion_prop
from lotion.properties import Relation


@notion_prop("タグ")
class TagRelation(Relation):
    def add(self, notion_page_id: str) -> "TagRelation":
        return TagRelation.from_id_list([*self.id_list, notion_page_id])
