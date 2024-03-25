from abc import ABCMeta, abstractmethod
from logging import Logger, getLogger

from common.service.scrape_service import ScrapeService
from common.service.tag_creator import TagCreator
from util.split_paragraph import split_paragraph
from util.tag_analyzer import TagAnalyzer
from util.text_summarizer import TextSummarizer
from webclip.domain.site_kind import SiteKind
from webclip.domain.webclip import Webclip


class WebclipGenerator(metaclass=ABCMeta):
    @abstractmethod
    def execute(
            self,
            url: str,
            title: str,
            cover: str | None = None) -> Webclip:
        """Webclipを生成する"""

class DefaultWebclipGenerator(WebclipGenerator):
    """通常のWebclipを生成するクラス"""
    def __init__(  # noqa: PLR0913
            self,
            scrape_service: ScrapeService,
            tag_creator: TagCreator,
            logger: Logger | None = None,
            tag_analyzer: TagAnalyzer | None = None,
            text_summarizer: TextSummarizer | None = None,
            ) -> None:
        self._scrape_service = scrape_service
        self._tag_creator = tag_creator
        self._tag_analyzer = tag_analyzer or TagAnalyzer()
        self._text_summarizer = text_summarizer or TextSummarizer()
        self._logger = logger or getLogger(__name__)

    def execute(
            self,
            url: str,
            title: str,
            cover: str | None = None,
            ) -> Webclip:
        # スクレイピングして要約を作成
        scraped_result = self._scrape_service.execute(url=url)
        page_text = scraped_result.not_formatted_text
        summary = self._text_summarizer.handle(page_text)

        # 要約からタグを抽出して、タグを作成
        tags = self._tag_analyzer.handle(text=summary)
        tag_relation = self._tag_creator.execute(name_list=tags)

        # ページ本文
        blocks = split_paragraph(page_text)

        # あたらしくWebclipを作成
        return Webclip.create(
            title=title,
            url=url,
            tag_relation=tag_relation,
            cover=cover,
            summary=summary,
            blocks=blocks,
        )

class TwitterWebclipGenerator(WebclipGenerator):
    """TwitterのWebclipを生成するクラス"""
    def __init__(
            self,
            tag_creator: TagCreator,
            tag_analyzer: TagAnalyzer | None = None,
            logger: Logger | None = None,
            ) -> None:
        self._tag_creator = tag_creator
        self._tag_analyzer = tag_analyzer or TagAnalyzer()
        self._logger = logger or getLogger(__name__)

    def execute(
            self,
            url: str,
            title: str,
            cover: str | None = None,
            ) -> Webclip:
        summary = title # 本文(title)をそのまま要約として扱う
        shorten_title = title[:50] # タイトルは本文(title)の50文字まで

        # 要約(本文)からタグを抽出して、タグを作成
        tags = self._tag_analyzer.handle(text=summary)
        tag_relation = self._tag_creator.execute(name_list=tags)

        # ページ本文
        blocks = split_paragraph(summary)

        # あたらしくWebclipを作成
        return Webclip.create(
            title=shorten_title,
            url=url,
            tag_relation=tag_relation,
            cover=cover,
            summary=summary,
            blocks=blocks,
        )

class WebclipGeneratorRule:
    def __init__(self, generator_dict: dict[SiteKind, WebclipGenerator]) -> None:
        self.generator_dict = generator_dict


    def get_generator(self, url: str) -> WebclipGenerator:
        """WebclipGeneratorを取得する"""
        site_kind = SiteKind.find_site_kind(url=url)
        return self.generator_dict[site_kind]
