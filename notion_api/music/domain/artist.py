from lotion.properties import Text


class Artist(Text):
    NAME = "Artist"

    @staticmethod
    def from_str_list(str_list: list[str]) -> "Artist":
        text_model = Text.from_plain_text(name=Artist.NAME, text=", ".join(str_list))
        return Artist(
            name=text_model.name,
            rich_text=text_model.rich_text,
        )

    @staticmethod
    def from_str(artists: str) -> "Artist":
        return Artist.from_str_list(artists.split(","))
