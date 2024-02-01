from typing import Optional
from datetime import date as Date
from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Title, Text, Relation, Url, Date, Cover
from notion_client_wrapper.block.rich_text.rich_text_builder import RichTextBuilder
from notion_client_wrapper.block import Paragraph
from usecase.service.tag_create_service import TagCreateService
from custom_logger import get_logger

logger = get_logger(__name__)

class AddTrackPageUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()
        self.tag_create_service = TagCreateService()

    def execute(self,
                track_name: str,
                artists: list[str],
                spotify_url: Optional[str] = None,
                cover_url: Optional[str] = None,
                release_date: Optional[Date] = None,
                ) -> dict:
        logger.info("execute")
        logger.info(f"track_name: {track_name}")
        logger.info(f"artists: {artists}")
        logger.info(f"spotify_url: {spotify_url}")
        logger.info(f"cover_url: {cover_url}")
        logger.info(f"release_date: {release_date}")

        # データベースの取得
        searched_musics = self.client.retrieve_database(
            database_id=DatabaseType.MUSIC.value,
            title=track_name,
        )
        if len(searched_musics) > 0:
            logger.info("Track is already registered")
            music = searched_musics[0]
            return {
                "id": music.id,
                "url": music.url
            }
        logger.info("Create a track page")

        # タグを作成
        tag_page_ids:list[str] = []
        for artist in artists:
            page_id = self.tag_create_service.add_tag(name=artist)
            tag_page_ids.append(page_id)

        # 新しいページを作成
        artist_name = ",".join(artists)
        properties=[
                Title.from_plain_text(name="名前", text=track_name),
                Text.from_plain_text(name="Artist", text=artist_name),
            ]
        if spotify_url is not None:
            properties.append(Url.from_url(name="Spotify", url=spotify_url))
        if len(tag_page_ids) > 0:
            properties.append(Relation.from_id_list(name="タグ", id_list=tag_page_ids))
        if release_date is not None:
            properties.append(Date.from_start_date(name="リリース日", start_date=release_date))
        result = self.client.create_page_in_database(
            database_id=DatabaseType.MUSIC.value,
            cover=Cover.from_external_url(cover_url) if cover_url is not None else None,
            properties=properties
        )
        page_id = result["id"]
        page_url = result["url"]

        iframe_html = _spotify_iframe_html(spotify_url=spotify_url)
        if iframe_html is not None:
            self.client.append_block(
                block_id=page_id,
                block=iframe_html
            )
        return {
            "id": page_id,
            "url": page_url
        }

def _spotify_iframe_html(spotify_url: Optional[str] = None) -> Optional[Paragraph]:
    if spotify_url is None:
        return None
    track_id = spotify_url.split("/")[-1].split("?")[0]
    iframe_html = f"""<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/{track_id}?utm_source=generator" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
    rich_text_builder = RichTextBuilder()
    rich_text_builder.add_text(iframe_html)
    rich_text = rich_text_builder.build()
    paragraph = Paragraph.from_rich_text(rich_text=rich_text)
    return paragraph

if __name__ == "__main__":
    # python -m usecase.add_track_page_usecase
    print(_spotify_iframe_html("https://open.spotify.com/intl-ja/track/5yCjgnILdfwZkNsh50eFGc?si=0faaf39670834b5c"))
