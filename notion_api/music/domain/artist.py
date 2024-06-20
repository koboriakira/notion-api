from notion_client_wrapper.properties.text import Text


class Artist(Text):
    NAME = "Artist"

    @classmethod
    def from_str_list(cls: "Artist", str_list: list[str]) -> "Artist":
        text_model = Text.from_plain_text(name=cls.NAME, text=", ".join(str_list))
        return cls(
            name=text_model.name,
            rich_text=text_model.rich_text,
        )
