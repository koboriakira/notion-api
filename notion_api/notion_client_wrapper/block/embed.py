from notion_client_wrapper.block.block import Block


class Embed(Block):
    caption: list
    embed_url: str

    def __init__(  # noqa: PLR0913
            self,
            embed_url: str,
            caption: list|None = None,
            id: str | None = None,  # noqa: A002
            archived: bool | None = None,
            created_time: str | None = None,
            last_edited_time: str | None = None,
            has_children: bool | None = None,
            parent: dict | None = None,
            ) -> None:
        super().__init__(id, archived, created_time, last_edited_time, has_children, parent)
        self.embed_url = embed_url
        self.caption = caption or []

    @staticmethod
    def of(block: dict) -> "Embed":
        embed = block["embed"]
        return Embed(
            id=block["id"],
            archived=block["archived"],
            created_time=block["created_time"],
            last_edited_time=block["last_edited_time"],
            has_children=block["has_children"],
            parent=block["parent"],
            caption=embed["caption"],
            embed_url=embed.get("url", ""),
        )

    @property
    def type(self) -> str:
        return "embed"

    def to_dict_sub(self) -> dict:
        raise NotImplementedError

    def to_slack_text(self) -> str:
        return self.embed_url
