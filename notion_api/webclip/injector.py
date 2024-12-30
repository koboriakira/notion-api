from lotion import Lotion

from common.injector import CommonInjector
from common.service.tag_creator import TagCreator
from common.value.site_kind import SiteKind
from custom_logger import get_logger
from util.openai_executer import OpenaiExecuter
from util.tag_analyzer import TagAnalyzer
from util.text_summarizer import TextSummarizer
from webclip.webclip_creator import WebclipCreator
from webclip.webclip_generator import (
    DefaultWebclipGenerator,
    TwitterWebclipGenerator,
    WebclipGenerator,
    WebclipGeneratorRule,
)

logger = get_logger(__name__)
client = Lotion.get_instance()
scrape_service = CommonInjector.get_scrape_service()
tag_creator = TagCreator(client=client)
openai_executer = OpenaiExecuter(logger=logger)
tag_analyzer = TagAnalyzer(client=openai_executer, logger=logger)
text_summarizer = TextSummarizer(client=openai_executer, logger=logger)
tweet_fetcher = CommonInjector.get_tweet_fetcher()


class WebclipInjector:
    @staticmethod
    def create_webclip_creator() -> WebclipCreator:
        webclip_generator_rule = WebclipInjector._create_webclip_generator_rule()
        return WebclipCreator(
            webclip_generator_rule=webclip_generator_rule,
            logger=logger,
        )

    @staticmethod
    def _create_webclip_generator_rule() -> WebclipGeneratorRule:
        generator_dict = {}
        for site_kind in SiteKind:
            generator_dict[site_kind] = WebclipInjector.__create_webclip_generator(site_kind)
        return WebclipGeneratorRule(generator_dict=generator_dict)

    @staticmethod
    def __create_webclip_generator(site_kind: SiteKind) -> WebclipGenerator:
        match site_kind:
            # TwitterまたはX
            case SiteKind.TWITTER | SiteKind.X:
                return TwitterWebclipGenerator(
                    tweet_fetcher=tweet_fetcher,
                    tag_creator=tag_creator,
                    tag_analyzer=tag_analyzer,
                    logger=logger,
                )
            case _:
                return DefaultWebclipGenerator(
                    scrape_service=scrape_service,
                    tag_creator=tag_creator,
                    tag_analyzer=tag_analyzer,
                    text_summarizer=text_summarizer,
                    logger=logger,
                )
