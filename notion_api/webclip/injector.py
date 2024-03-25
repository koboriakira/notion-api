from common.injector import CommonInjector
from common.service.tag_creator import TagCreator
from custom_logger import get_logger
from notion_client_wrapper.client_wrapper import ClientWrapper
from util.openai_executer import OpenaiExecuter
from util.tag_analyzer import TagAnalyzer
from util.text_summarizer import TextSummarizer
from webclip.domain.site_kind import SiteKind
from webclip.infrastructure.webclip_repository_impl import WebclipRepositoryImpl
from webclip.service.webclip_creator import WebclipCreator
from webclip.service.webclip_generator import (
    DefaultWebclipGenerator,
    TwitterWebclipGenerator,
    WebclipGenerator,
    WebclipGeneratorRule,
)

logger = get_logger(__name__)
client = ClientWrapper.get_instance()
scrape_service = CommonInjector.get_scrape_service()
tag_creator = TagCreator(client=client)
openai_executer = OpenaiExecuter(logger=logger)
tag_analyzer = TagAnalyzer(client=openai_executer, logger=logger)
text_summarizer = TextSummarizer(client=openai_executer, logger=logger)

class WebclipInjector:
    @classmethod
    def create_webclip_creator(cls: "WebclipInjector") -> WebclipCreator:
        webclip_repository = WebclipRepositoryImpl(client=client, logger=logger)
        webclip_generator_rule = cls._create_webclip_generator_rule()
        return WebclipCreator(
            webclip_repository=webclip_repository,
            webclip_generator_rule=webclip_generator_rule,
            logger=logger,
        )

    @classmethod
    def _create_webclip_generator_rule(cls: "WebclipInjector") -> WebclipGeneratorRule:
        generator_dict = {}
        for site_kind in SiteKind:
            generator_dict[site_kind] = cls.__create_webclip_generator(site_kind)
        return WebclipGeneratorRule(generator_dict=generator_dict)


    @classmethod
    def __create_webclip_generator(cls: "WebclipInjector", site_kind: SiteKind) -> WebclipGenerator:
        match site_kind:
            case SiteKind.TWITTER:
                return TwitterWebclipGenerator(
                    tag_creator=tag_creator,
                    tag_analyzer=tag_analyzer,
                    logger=logger,
                )
            case SiteKind.DEFAULT:
                return DefaultWebclipGenerator(
                    scrape_service=scrape_service,
                    tag_creator=tag_creator,
                    tag_analyzer=tag_analyzer,
                    text_summarizer=text_summarizer,
                    logger=logger,
                )
            case _:
                msg = f"Unexpected site_kind: {site_kind}"
                raise ValueError(msg)
