from dataclasses import dataclass
from datetime import date

from lotion.base_page import BasePage
from lotion.block import Block
from lotion.properties import Cover, Properties

from common.domain.tag_relation import TagRelation
from music.domain.artist import Artist
from music.domain.release_date import ReleaseDate
from music.domain.song_title import SongTitle
from music.domain.spotify_url import SpotifyUrl


@dataclass
class Song(BasePage):
    @staticmethod
    def create(
        title: str | SongTitle,
        artist: str | Artist,
        spotify_url: str | SpotifyUrl | None = None,
        tag_relation: list[str] | TagRelation | None = None,
        release_date: date | ReleaseDate | None = None,
        blocks: list[Block] | None = None,
        cover: str | Cover | None = None,
    ) -> "Song":
        blocks = blocks or []
        properties = [
            title if isinstance(title, SongTitle) else SongTitle(text=title),
            spotify_url if isinstance(spotify_url, SpotifyUrl) else SpotifyUrl(url=spotify_url),
            artist if isinstance(artist, Artist) else Artist.from_str(artists=artist),
        ]
        if tag_relation is not None:
            tag_relation = (
                tag_relation
                if isinstance(tag_relation, TagRelation)
                else TagRelation.from_id_list(id_list=tag_relation)
            )
            properties.append(tag_relation)

        if release_date is not None:
            release_date = release_date if isinstance(release_date, ReleaseDate) else ReleaseDate(date_=release_date)
            properties.append(release_date)

        if cover is None:
            return Song(properties=Properties(values=properties), block_children=blocks)
        cover = cover if isinstance(cover, Cover) else Cover.from_external_url(cover)
        return Song(properties=Properties(values=properties), block_children=blocks, cover=cover)

    def update_tag_relation(self, tag_relation: TagRelation) -> None:
        properties = self.properties.append_property(tag_relation)
        self.properties = properties

    @property
    def song_title(self) -> str:
        return self.get_title_text()

    @property
    def spotify_url(self) -> str:
        return self.get_url(name=SpotifyUrl.NAME).url.split("?")[0]

    @property
    def tag_relation(self) -> list[str]:
        return self.get_relation(TagRelation.NAME).id_list

    @property
    def artist(self) -> str:
        return self.get_text(name=Artist.NAME).text

    @property
    def release_date(self) -> date | None:
        return self.get_date(name=ReleaseDate.NAME).start_date

    @property
    def spotify_track_id(self) -> str:
        # https://open.spotify.com/intl-ja/track/0VfOZBCILsIrkJPzw3WdvA?si=731d95eb095543ac からクエリを除いた部分
        return self.spotify_url.split("/")[-1].split("?")[0]

    @property
    def embed_html(self) -> str:
        text = f"""<iframe style="border-radius:12px"
 src="https://open.spotify.com/embed/track/{self.spotify_track_id}?utm_source=generator"
 width="100%" height="152"
 frameBorder="0"
 allowfullscreen=""
 allow="autoplay;
 clipboard-write;
 encrypted-media;
 fullscreen;
 picture-in-picture"
 loading="lazy">
</iframe>
"""
        return text.replace("\n", "")
