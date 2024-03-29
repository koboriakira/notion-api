from notion_client_wrapper.block.block import Block


class Image(Block):
    image_caption: list
    image_type: str
    image_file: dict
    type: str = "image"

    def __init__(
        self,
        image_caption: list,
        image_type: str,
        image_file: dict,
        id: str | None = None,  # noqa: A002
        archived: bool | None = None,
        created_time: str | None = None,
        last_edited_time: str | None = None,
        has_children: bool | None = None,
        parent: dict | None = None,
    ):
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)
        self.image_caption = image_caption
        self.image_type = image_type
        self.image_file = image_file

    @staticmethod
    def of(block: dict) -> "Image":
        image = block["image"]
        image_caption = image.get("caption", [])
        image_type = image.get("type", "")
        image_file = image.get("file", {})
        return Image(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            image_caption=image_caption,
            image_type=image_type,
            image_file=image_file,
        )

    @property
    def type(self) -> str:
        return "image"

    def to_dict_sub(self) -> dict:
        raise NotImplementedError

    def to_slack_text(self) -> str:
        return ""
