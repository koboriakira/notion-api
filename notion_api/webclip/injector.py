from common.injector import CommonInjector
from common.service.tag_creator import TagCreator
from custom_logger import get_logger
from notion_client_wrapper.client_wrapper import ClientWrapper
from util.openai_executer import OpenaiExecuter
from util.tag_analyzer import TagAnalyzer
from util.text_summarizer import TextSummarizer
from webclip.infrastructure.webclip_repository_impl import WebclipRepositoryImpl
from webclip.service.webclip_creator import WebclipCreator

logger = get_logger(__name__)

class WebclipInjector:
    @staticmethod
    def create_webclip_creator() -> WebclipCreator:
        client = ClientWrapper.get_instance()
        webclip_repository = WebclipRepositoryImpl(client=client, logger=logger)
        scrape_service = CommonInjector.get_scrape_service()
        tag_creator = TagCreator(client=client)
        openai_executer = OpenaiExecuter(logger=logger)
        tag_analyzer = TagAnalyzer(client=openai_executer, logger=logger)
        text_summarizer = TextSummarizer(client=openai_executer, logger=logger)
        return WebclipCreator(
            webclip_repository=webclip_repository,
            scrape_service=scrape_service,
            logger=logger,
            tag_creator=tag_creator,
            tag_analyzer=tag_analyzer,
            text_summarizer=text_summarizer,
        )
