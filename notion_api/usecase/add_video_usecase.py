from typing import Optional
from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Title, Relation, Url, Cover
from notion_client_wrapper.block import Paragraph
from usecase.service.tag_create_service import TagCreateService
from infrastructure.slack_bot_client import SlackBotClient
from infrastructure.slack_user_client import SlackUserClient
from custom_logger import get_logger

logger = get_logger(__name__)

class AddVideoUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()
        self.slack_bot_client = SlackBotClient()
        self.slack_user_client = SlackUserClient()
        self.tag_create_service = TagCreateService()

    def execute(
            self,
            url: str,
            title: str,
            tags: list[str],
            cover: Optional[str] = None,
            slack_channel: Optional[str] = None,
            slack_thread_ts: Optional[str] = None,
            ) -> dict:
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

        self._append_embed_code(block_id=result["id"], url=url)

        self.slack_user_client.update_context(
            channel=slack_channel,
            ts=slack_thread_ts,
            context={
                "page_id": result["id"]
            }
        )

        self.slack_bot_client.send_message(
            channel=slack_channel,
            text=f"動画を追加しました: {result['url']}",
            thread_ts=slack_thread_ts,
        )

        return {
            "id": result["id"],
            "url": result["url"]
        }

    def _append_embed_code(self, block_id: str, url: str) -> None:
        if "youtube.com" not in url:
            return

        video_id = None
        for query_param in url.split("?")[1].split("&"):
            key, value = query_param.split("=")
            if key == "v":
                video_id = value
                break
        if video_id is None:
            raise ValueError("Invalid URL")

        embed_code = f"""<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>"""
        paragraph = Paragraph.from_plain_text(text=embed_code)
        self.client.append_block(block_id=block_id, block=paragraph)

if __name__ == "__main__":
    # python -m usecase.add_video_usecase
    usecase = AddVideoUsecase()
    usecase._append_embed_code(
        url="https://youtube.com/watch?v=7u1EehDMwF4&amp;si=rqajmV4iuicBKDfD",
        block_id="cd97c02a25e94bb980fe67a02c874ac2"
    )
