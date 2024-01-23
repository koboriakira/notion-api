from typing import Optional
from datetime import date as Date
from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Title, Text, Relation, Url, Date, Cover
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
        return {
            "id": result["id"],
            "url": result["url"]
        }
