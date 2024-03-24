
from common.service.scrape_service import ScrapeService
from custom_logger import get_logger
from domain.database_type import DatabaseType
from notion_client_wrapper.block import Paragraph
from notion_client_wrapper.block.rich_text.rich_text_builder import RichTextBuilder
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Cover, Relation, Text, Title, Url
from slack_concierge.service.append_context_service import AppendContextService
from usecase.service.inbox_service import InboxService
from usecase.service.tag_analyzer import TagAnalyzer
from usecase.service.tag_create_service import TagCreateService
from usecase.service.text_summarizer import TextSummarizer

logger = get_logger(__name__)

class AddWebclipUsecase:
    def __init__(  # noqa: PLR0913
            self,
            scrape_service: ScrapeService,
            inbox_service: InboxService,
            append_context_service: AppendContextService,
            tag_create_service: TagCreateService,
            tag_analyzer: TagAnalyzer) -> None:
        self._scrape_service = scrape_service
        self._inbox_service = inbox_service
        self._append_context_service = append_context_service
        self._tag_create_service = tag_create_service
        self._tag_analyzer = tag_analyzer
        self.text_summarizer = TextSummarizer()
        self.client = ClientWrapper.get_instance()

    def execute(  # noqa: C901, PLR0913
            self,
            url: str,
            title: str,
            cover: str | None = None,
            slack_channel: str | None = None,
            slack_thread_ts: str | None = None,
            ) -> dict:
        logger.info("execute")

        searched_webclips = self.client.retrieve_database(
            database_id=DatabaseType.WEBCLIP.value,
            title=title,
        )
        if len(searched_webclips) > 0:
            logger.info("Webclip is already registered")
            page = searched_webclips[0]
            return {
                "id": page.id,
                "url": page.url,
            }
        logger.info("Create a Webclip")

        if "twitter.com" in url:
            return self._handle_for_twitter(
                url=url,
                title=title,
                cover=cover,
                slack_channel=slack_channel,
                slack_thread_ts=slack_thread_ts,
            )

        # スクレイピングして要約を作成
        scraped_result = self._scrape_service.execute(url=url)
        page_text = scraped_result.not_formatted_text
        summary = self.text_summarizer.handle(page_text)

        # 要約からタグを抽出して、タグを作成
        tag_page_ids:list[str] = []
        tags = self._tag_analyzer.handle(text=summary)
        for tas in tags:
            page_id = self._tag_create_service.add_tag(name=tas)
            tag_page_ids.append(page_id)

        # 新しいページを作成
        properties=[
                Title.from_plain_text(name="名前", text=title),
                Url.from_url(name="URL", url=url),
            ]
        if len(tag_page_ids) > 0:
            properties.append(Relation.from_id_list(name="タグ", id_list=tag_page_ids))
        if summary is not None:
            properties.append(Text.from_plain_text(name="概要", text=summary))
        result = self.client.create_page_in_database(
            database_id=DatabaseType.WEBCLIP.value,
            cover=Cover.from_external_url(cover) if cover is not None else None,
            properties=properties,
        )
        page_id = result["id"]
        page_url = result["url"]

        self._inbox_service.add_inbox_task_by_page_id(
            page_id=page_id,
            page_url=page_url,
            original_url=url,
            slack_channel=slack_channel,
            slack_thread_ts=slack_thread_ts,
        )
        self._append_context_service.append_page_id(
            channel=slack_channel,
            event_ts=slack_thread_ts,
            page_id=page_id,
        )

        # ページ本文を追加
        if page_text is not None:
            # textが1500文字を超える場合は、1500文字ずつ分割して追加する
            if len(page_text) > 1500:
                for i in range(0, len(page_text), 1500):
                    rich_text = RichTextBuilder.get_instance().add_text(page_text[i:i+1500]).build()
                    paragraph = Paragraph.from_rich_text(rich_text=rich_text)
                    self.client.append_block(block_id=page_id, block=paragraph)
            else:
                rich_text = RichTextBuilder.get_instance().add_text(page_text).build()
                paragraph = Paragraph.from_rich_text(rich_text=rich_text)
                self.client.append_block(block_id=page_id, block=paragraph)
        return {
            "id": page_id,
            "url": page_url,
        }

    def _handle_for_twitter(  # noqa: PLR0913
            self,
            url: str,
            title: str, # ツイート本文
            cover: str | None = None,
            slack_channel: str | None = None,
            slack_thread_ts: str | None = None,
            ) -> dict:
        # Twitter本文からタグを抽出して、タグを作成
        tag_page_ids:list[str] = []
        tags = self._tag_analyzer.handle(text=title)
        for tas in tags:
            page_id = self._tag_create_service.add_tag(name=tas)
            tag_page_ids.append(page_id)

        # 新しいページを作成
        properties=[
                Title.from_plain_text(name="名前", text=title[:50]),
                Url.from_url(name="URL", url=url),
                Text.from_plain_text(name="概要", text=title),
            ]
        if len(tag_page_ids) > 0:
            properties.append(Relation.from_id_list(name="タグ", id_list=tag_page_ids))

        result = self.client.create_page_in_database(
            database_id=DatabaseType.WEBCLIP.value,
            cover=Cover.from_external_url(cover) if cover is not None else None,
            properties=properties,
        )
        page_id = result["id"]
        page_url = result["url"]

        self._inbox_service.add_inbox_task_by_page_id(
            page_id=page_id,
            page_url=page_url,
            original_url=url,
            slack_channel=slack_channel,
            slack_thread_ts=slack_thread_ts,
        )
        self._append_context_service.append_page_id(
            channel=slack_channel,
            event_ts=slack_thread_ts,
            page_id=page_id,
        )

        return {
            "id": page_id,
            "url": page_url,
        }
