from lotion import notion_prop
from lotion.properties import Text


@notion_prop("Artist")
class Artist(Text):
    @staticmethod
    def from_str_list(str_list: list[str]) -> "Artist":
        return Artist.from_plain_text(text=", ".join(str_list))

    @staticmethod
    def from_str(artists: str) -> "Artist":
        return Artist.from_str_list(artists.split(","))
