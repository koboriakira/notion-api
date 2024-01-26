from typing import Optional
from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Title, Relation, Url, Cover
from usecase.service.tag_create_service import TagCreateService
from custom_logger import get_logger

logger = get_logger(__name__)

class AddVideoUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()
        self.tag_create_service = TagCreateService()

    def execute(self,
                url: str,
                title: str,
               tags: list[str],
               cover: Optional[str] = None,
               ) -> dict:
        logger.info("execute")

        searched_videos = self.client.retrieve_database(
            database_id=DatabaseType.VIDEO.value,
            title=title,
        )
        if len(searched_videos) > 0:
            logger.info("Video is already registered")
            page = searched_videos[0]
            return {
                "id": page.id,
                "url": page.url
            }
        logger.info("Create a Video")

        # タグを作成
        tag_page_ids:list[str] = []
        for tas in tags:
            page_id = self.tag_create_service.add_tag(name=tas)
            tag_page_ids.append(page_id)

        # 新しいページを作成
        properties=[
                Title.from_plain_text(name="名前", text=title),
                Url.from_url(name="URL", url=url),
            ]
        if len(tag_page_ids) > 0:
            properties.append(Relation.from_id_list(name="タグ", id_list=tag_page_ids))
        result = self.client.create_page_in_database(
            database_id=DatabaseType.VIDEO.value,
            cover=Cover.from_external_url(cover) if cover is not None else None,
            properties=properties
        )
        return {
            "id": result["id"],
            "url": result["url"]
        }
