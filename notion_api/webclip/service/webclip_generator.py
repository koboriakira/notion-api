from abc import ABCMeta, abstractmethod
from logging import Logger, getLogger
from typing import TYPE_CHECKING

from lotion.block import Embed

from common.domain.tag_relation import TagRelation
from common.service.scrape_service import ScrapeService
from common.service.tag_creator import TagCreator
from common.service.tweet.tweet_fetcher import TweetFetcher
from common.value.site_kind import SiteKind
from util.split_paragraph import split_paragraph
from util.tag_analyzer import TagAnalyzer
from util.text_summarizer import TextSummarizer
from webclip.domain.webclip import Webclip
from webclip.service import webclip_creator

if TYPE_CHECKING:
    from lotion.block import Block


class WebclipGenerator(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, url: str, title: str, cover: str | None = None) -> Webclip:
        """Webclipを生成する"""


class DefaultWebclipGenerator(WebclipGenerator):
    """通常のWebclipを生成するクラス"""

    def __init__(
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

        # カバー画像が指定されてなければ取得を試みる
        cover = cover or scraped_result.get_image_url()

        # 要約からタグを抽出して、タグを作成
        tags = self._tag_analyzer.handle(text=summary)
        tag_page_id_list = self._tag_creator.execute(tag=tags)
        tag_relation = TagRelation.from_page_id_list(tag_page_id_list)

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
        tweet_fetcher: TweetFetcher,
        tag_creator: TagCreator,
        tag_analyzer: TagAnalyzer | None = None,
        logger: Logger | None = None,
    ) -> None:
        self._tweet_fetcher = tweet_fetcher
        self._tag_creator = tag_creator
        self._tag_analyzer = tag_analyzer or TagAnalyzer()
        self._logger = logger or getLogger(__name__)

    def execute(
        self,
        url: str,
        title: str,  # noqa: ARG002 FIXME: 利用しないパターンもある
        cover: str | None = None,
    ) -> Webclip:
        tweet_id = self._extract_tweet_id(url=url)
        tweet = self._tweet_fetcher.fetch(tweet_id)

        # 本文からタグを抽出して、タグを作成
        tags = self._tag_analyzer.handle(text=tweet.text)
        # 投稿者もタグに含める
        tags.append(tweet.user_name)
        tag_page_id_list = self._tag_creator.execute(tag=tags)
        tag_relation = TagRelation.from_page_id_list(tag_page_id_list)

        # カバー画像が指定されてなければ取得を試みる
        if not cover:
            cover = tweet.media_urls[0] if tweet.media_urls else None

        blocks: list[Block] = []
        # 本文を入れる
        blocks.extend(split_paragraph(tweet.text))
        # 画像をいれる
        for media_url in tweet.media_urls:
            embed = Embed.from_url_and_caption(url=media_url)
            blocks.append(embed)

        # あたらしくWebclipを作成
        return Webclip.create(
            title=tweet.text[:50],  # タイトルは本文(title)の50文字まで,
            url=tweet.url,
            tag_relation=tag_relation,
            cover=cover,
            summary=tweet.text,
            blocks=blocks,
        )

    def _extract_tweet_id(self, url: str) -> str:
        """URLからtweet_idを抽出する"""
        tweet_id = url.split("/status/")[1]
        return tweet_id.split("/")[0]


class WebclipGeneratorRule:
    def __init__(self, generator_dict: dict[SiteKind, WebclipGenerator]) -> None:
        self.generator_dict = generator_dict

    def get_generator(self, url: str) -> WebclipGenerator:
        """WebclipGeneratorを取得する"""
        site_kind = SiteKind.find_site_kind(url=url)
        return self.generator_dict[site_kind]


if __name__ == "__main__":
    # python -m notion_api.webclip.service.webclip_generator
    from webclip.injector import WebclipInjector

    webclip_creator = WebclipInjector.create_webclip_creator()

    twitter_url = "https://twitter.com/uug_p_STAFF/status/1772234517572722806"
    twitter_webclip_generator = webclip_creator._webclip_generator_rule.get_generator(twitter_url)  # noqa: SLF001
    twitter_webclip = twitter_webclip_generator.execute(url=twitter_url, title="")
    print(twitter_webclip)
