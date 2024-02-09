from typing import Optional
from datetime import date as Date
from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Title, Text, Relation, Url, Date, Cover, Status
from notion_client_wrapper.block.rich_text.rich_text_builder import RichTextBuilder
from notion_client_wrapper.block import Paragraph
from usecase.service.tag_create_service import TagCreateService
from usecase.service.tag_analyzer import TagAnalyzer
from usecase.service.simple_scraper import SimpleScraper
from usecase.service.text_summarizer import TextSummarizer
from usecase.service.inbox_service import InboxService
from custom_logger import get_logger

logger = get_logger(__name__)

class AddWebclipUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()
        self.tag_create_service = TagCreateService()
        self.tag_analyzer = TagAnalyzer()
        self.simple_scraper = SimpleScraper()
        self.text_summarizer = TextSummarizer()
        self.inbox_service = InboxService()

    def execute(
            self,
            url: str,
            title: str,
            cover: Optional[str] = None,
            slack_channel: Optional[str] = None,
            slack_thread_ts: Optional[str] = None,
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
                "url": page.url
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
        page_text, formatted_page_text = self.simple_scraper.handle(url=url)
        if page_text is None:
            raise Exception("ページのスクレイピングに失敗しました。")
        summary = self.text_summarizer.handle(page_text)

        # 要約からタグを抽出して、タグを作成
        tag_page_ids:list[str] = []
        tags = self.tag_analyzer.handle(text=summary)
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
        if summary is not None:
            properties.append(Text.from_plain_text(name="概要", text=summary))
        result = self.client.create_page_in_database(
            database_id=DatabaseType.WEBCLIP.value,
            cover=Cover.from_external_url(cover) if cover is not None else None,
            properties=properties
        )
        page = {
            "id": result["id"],
            "url": result["url"]
        }

        self.inbox_service.add_inbox_task_by_page_id(
            page_id=result["id"],
            page_url=result["url"],
            slack_channel=slack_channel,
            slack_thread_ts=slack_thread_ts
        )

        # ページ本文を追加
        if page_text is not None:
            # textが1500文字を超える場合は、1500文字ずつ分割して追加する
            if len(page_text) > 1500:
                for i in range(0, len(page_text), 1500):
                    rich_text = RichTextBuilder.get_instance().add_text(page_text[i:i+1500]).build()
                    paragraph = Paragraph.from_rich_text(rich_text=rich_text)
                    self.client.append_block(block_id=page["id"], block=paragraph)
            else:
                rich_text = RichTextBuilder.get_instance().add_text(page_text).build()
                paragraph = Paragraph.from_rich_text(rich_text=rich_text)
                self.client.append_block(block_id=page["id"], block=paragraph)
        return page

    def _handle_for_twitter(
            self,
            url: str,
            title: str, # ツイート本文
            cover: Optional[str] = None,
            slack_channel: Optional[str] = None,
            slack_thread_ts: Optional[str] = None,
            ) -> dict:
        # Twitter本文からタグを抽出して、タグを作成
        tag_page_ids:list[str] = []
        tags = self.tag_analyzer.handle(text=title)
        for tas in tags:
            page_id = self.tag_create_service.add_tag(name=tas)
            tag_page_ids.append(page_id)

        # 新しいページを作成
        properties=[
                Title.from_plain_text(name="名前", text=title[:50]),
                Url.from_url(name="URL", url=url),
                Text.from_plain_text(name="概要", text=title)
            ]
        if len(tag_page_ids) > 0:
            properties.append(Relation.from_id_list(name="タグ", id_list=tag_page_ids))

        result = self.client.create_page_in_database(
            database_id=DatabaseType.WEBCLIP.value,
            cover=Cover.from_external_url(cover) if cover is not None else None,
            properties=properties
        )
        page = {
            "id": result["id"],
            "url": result["url"]
        }

        self.inbox_service.add_inbox_task_by_page_id(
            page_id=result["id"],
            page_url=result["url"],
            slack_channel=slack_channel,
            slack_thread_ts=slack_thread_ts
        )

        return page
