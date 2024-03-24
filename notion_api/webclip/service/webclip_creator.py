from logging import Logger, getLogger

from common.domain.tag_relation import TagRelation
from common.service.scrape_service import ScrapeService
from common.service.tag_creator import TagCreator
from util.tag_analyzer import TagAnalyzer
from util.text_summarizer import TextSummarizer
from webclip.domain.webclip import Webclip
from webclip.infrastructure.webclip_repository_impl import WebclipRepositoryImpl


class WebclipCreator:
    def __init__(
            self,
            webclip_repository: WebclipRepositoryImpl,
            scrape_service: ScrapeService,
            tag_creator: TagCreator,
            logger: Logger | None = None,
            tag_analyzer: TagAnalyzer | None = None,
            text_summarizer: TextSummarizer | None = None,
            ) -> None:
        self._webclip_repository = webclip_repository
        self._scrape_service = scrape_service
        self._tag_creator = tag_creator
        self._logger = logger or getLogger(__name__)
        self._tag_analyzer = tag_analyzer or TagAnalyzer()
        self._text_summarizer = text_summarizer or TextSummarizer()


    def execute(  # noqa: PLR0913
            self,
            url: str,
            title: str,
            cover: str | None = None,
            slack_channel: str | None = None,
            slack_thread_ts: str | None = None,
            ) -> dict:
        info_message = f"{self.__class__} execute: url={url}, title={title}, cover={cover}, slack_channel={slack_channel}, slack_thread_ts={slack_thread_ts}"
        self._logger.info(info_message)

        webclip = self._webclip_repository.find_by_title(title=title)
        if webclip is not None:
            info_message = f"Webclip is already registered: {webclip.get_title_text()}"
            self._logger.info(info_message)
            return {
                "id": webclip.id,
                "url": webclip.url,
            }

        info_message = "Create a Webclip"
        self._logger.info(info_message)

        # スクレイピングして要約を作成
        scraped_result = self._scrape_service.execute(url=url)
        page_text = scraped_result.not_formatted_text
        summary = self._text_summarizer.handle(page_text)

        tag_relation = TagRelation.empty()

        # 要約からタグを抽出して、タグを作成
        tags = self._tag_analyzer.handle(text=summary)
        for tag in tags:
            tag_page_id = self._tag_creator.execute(name=tag)
            tag_relation = tag_relation.add(tag_page_id)

        # あたらしくWebclipを作成
        webclip = Webclip.create(
            title=title,
            url=url,
            tag_relation=tag_relation,
            cover=cover,
            summary=summary, # FIXME: あとでいれる
        )
        webclip = self._webclip_repository.save(webclip=webclip)
        return {
            "id": webclip.id,
            "url": webclip.url,
        }


if __name__ == "__main__":
    # python -m notion_api.webclip.service.webclip_creator
    from webclip.injector import WebclipInjector
    service = WebclipInjector.create_webclip_creator()
    service.execute(
        url="https://hobby.dengeki.com/news/2222026/",
        title="『爆走兄弟レッツ＆ゴー!!』のミニ四駆がミニカー化！マグナムセイバーなどの「トミカプレミアムunlimited」がAmazonで予約受付中!! | 電撃ホビーウェブ",
    )
