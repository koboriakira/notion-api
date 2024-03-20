
from notion_client_wrapper.block.block import Block
from notion_client_wrapper.block.rich_text import RichText


class BulletedlistItem(Block):
    rich_text: RichText
    color: str

    def __init__(
            self,
            rich_text: RichText,
            color: str|None = None,
            id: str|None = None,
            archived: bool|None = None,
            created_time: str|None = None,
            last_edited_time: str|None = None,
            has_children: bool|None = None,
            parent: dict|None = None):
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)
        self.rich_text = rich_text
        self.color = color

    @staticmethod
    def of(block: dict) -> "BulletedlistItem":
        bulleted_list_item = block["bulleted_list_item"]
        rich_text = RichText.from_entity(bulleted_list_item["rich_text"])
        return BulletedlistItem(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            rich_text=rich_text,
            color=bulleted_list_item["color"],
        )

    def to_slack_text(self) -> str:
        return f"- {self.rich_text.to_slack_text()}"

    @staticmethod
    def from_rich_text(rich_text: RichText) -> "BulletedlistItem":
        return BulletedlistItem(rich_text=rich_text)

    @property
    def type(self) -> str:
        return "bulleted_list_item"

    def to_dict_sub(self) -> dict:
        result = {
            "rich_text": self.rich_text.to_dict(),
        }
        if self.color is not None:
            result["color"] = self.color
        return result
