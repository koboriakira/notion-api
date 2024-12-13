from lotion.properties import Text


class Artist(Text):
    NAME = "Artist"

    @classmethod
    def from_str_list(cls: "Artist", str_list: list[str]) -> "Artist":
        text_model = Text.from_plain_text(name=cls.NAME, text=", ".join(str_list))
        return cls(
            name=text_model.name,
            rich_text=text_model.rich_text,
        )

    @classmethod
    def from_str(cls: "Artist", artists: str) -> "Artist":
        return Artist.from_str_list(artists.split(","))
