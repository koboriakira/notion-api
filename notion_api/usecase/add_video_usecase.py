
from custom_logger import get_logger
from domain.database_type import DatabaseType
from notion_client_wrapper.block import Paragraph
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Cover, Relation, Title, Url
from usecase.service.append_page_id_to_slack_context import AppendPageIdToSlackContext
from usecase.service.inbox_service import InboxService
from usecase.service.tag_analyzer import TagAnalyzer
from usecase.service.tag_create_service import TagCreateService

logger = get_logger(__name__)

class AddVideoUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()
        self.inbox_service = InboxService()
        self.tag_analyzer = TagAnalyzer()
        self.tag_create_service = TagCreateService()
        self.append_page_id_to_slack_context = AppendPageIdToSlackContext()

    def execute(
            self,
            url: str,
            title: str,
            cover: str | None = None,
            slack_channel: str | None = None,
            slack_thread_ts: str | None = None,
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
                "url": page.url,
            }
        logger.info("Create a Video")

        tags = self.tag_analyzer.handle(text=title)

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
            properties=properties,
        )
        page_id = result["id"]
        page_url = result["url"]

        self._append_embed_code(block_id=page_id, url=url)

        self.inbox_service.add_inbox_task_by_page_id(
            page_id=page_id,
            page_url=page_url,
            original_url=url,
            slack_channel=slack_channel,
            slack_thread_ts=slack_thread_ts,
        )
        self.append_page_id_to_slack_context.execute(
            channel=slack_channel,
            event_ts=slack_thread_ts,
            page_id=page_id,
        )

        return {
            "id": page_id,
            "url": page_url,
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
        block_id="cd97c02a25e94bb980fe67a02c874ac2",
    )
