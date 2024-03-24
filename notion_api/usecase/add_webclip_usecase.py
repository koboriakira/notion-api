
from common.service.scrape_service import ScrapeService
from custom_logger import get_logger
from domain.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_client_wrapper.properties import Cover, Relation, Text, Title, Url
from slack_concierge.service.append_context_service import AppendContextService
from usecase.service.inbox_service import InboxService
from usecase.service.tag_analyzer import TagAnalyzer
from usecase.service.tag_create_service import TagCreateService
from usecase.service.text_summarizer import TextSummarizer
from webclip.service.webclip_creator import WebclipCreator

logger = get_logger(__name__)

class AddWebclipUsecase:
    def __init__(  # noqa: PLR0913
            self,
            webclip_creator: WebclipCreator,
            scrape_service: ScrapeService,
            inbox_service: InboxService,
            append_context_service: AppendContextService,
            tag_create_service: TagCreateService,
            tag_analyzer: TagAnalyzer,
            text_summarizer: TextSummarizer,
            client: ClientWrapper) -> None:
        self._webclip_creator = webclip_creator
        self._scrape_service = scrape_service
        self._inbox_service = inbox_service
        self._append_context_service = append_context_service
        self._tag_create_service = tag_create_service
        self._tag_analyzer = tag_analyzer
        self._text_summarizer = text_summarizer
        self._client = client

    def execute(  # noqa: PLR0913
            self,
            url: str,
            title: str,
            cover: str | None = None,
            slack_channel: str | None = None,
            slack_thread_ts: str | None = None,
            ) -> dict:
        if "twitter.com" in url:
            return self._handle_for_twitter(
                url=url,
                title=title,
                cover=cover,
                slack_channel=slack_channel,
                slack_thread_ts=slack_thread_ts,
            )

        webclip = self._webclip_creator.execute(
            url=url,
            title=title,
            cover=cover,
        )

        self._inbox_service.add_inbox_task_by_page_id(
            page_id=webclip.id,
            page_url=webclip.url,
            original_url=url,
            slack_channel=slack_channel,
            slack_thread_ts=slack_thread_ts,
        )
        self._append_context_service.append_page_id(
            channel=slack_channel,
            event_ts=slack_thread_ts,
            page_id=webclip.id,
        )

        return {
            "id": webclip.id,
            "url": webclip.url,
        }

    def _handle_for_twitter(  # noqa: PLR0913
            self,
            url: str,
            title: str, # ツイート本文
            cover: str | None = None,
            slack_channel: str | None = None,
            slack_thread_ts: str | None = None,
            ) -> dict:
        logger.info("execute(twitter)")

        title_property = Title.from_plain_text(name="名前", text=title)
        filter_param = FilterBuilder.build_simple_equal_condition(title_property)

        searched_webclips = self._client.retrieve_database(
            database_id=DatabaseType.WEBCLIP.value,
            filter_param=filter_param,
        )
        if len(searched_webclips) > 0:
            logger.info("Webclip is already registered")
            page = searched_webclips[0]
            return {
                "id": page.id,
                "url": page.url,
            }

        logger.info("Create a Webclip")
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

        result = self._client.create_page_in_database(
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

if __name__ == "__main__":
    # python -m notion_api.usecase.add_webclip_usecase
    from injector.injector import Injector
    usecase = Injector.create_add_webclip_usecase()
    usecase.execute(
        url="https://speakerdeck.com/yuitosato/functional-and-type-safe-ddd-for-oop",
        title="ビジネスロジックを「型」で表現するOOPのための関数型DDD / Functional And Type-Safe DDD for OOP",
        slack_channel="C05GUTE35RU",
        slack_thread_ts="1711238809.901419",
    )
