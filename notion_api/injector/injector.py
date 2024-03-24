from logging import Logger

from slack_sdk.web import WebClient

from common.injector import CommonInjector
from custom_logger import get_logger
from notion_client_wrapper.client_wrapper import ClientWrapper
from slack_concierge.injector import SlackConciergeInjector
from usecase.add_webclip_usecase import AddWebclipUsecase
from usecase.service.inbox_service import InboxService
from usecase.service.tag_analyzer import TagAnalyzer
from usecase.service.tag_create_service import TagCreateService
from usecase.service.text_summarizer import TextSummarizer
from util.openai_executer import OpenaiExecuter

logger = get_logger(__name__)

DEFAULT_GPT_MODEL = "gpt-3.5-turbo-1106"

class Injector:
    @classmethod
    def create_add_webclip_usecase(cls: "Injector") -> AddWebclipUsecase:
        openai_executer = cls.__create_openai_executer(model=DEFAULT_GPT_MODEL, logger=logger)
        scrape_service = CommonInjector.get_scrape_service()
        inbox_service = cls.create_inbox_service()
        tag_create_service = cls.create_tag_create_service()
        tag_analyzer = cls.create_tag_analyzer(
            openai_executer=openai_executer,
            is_debug=False)
        text_summarizer = cls.create_text_summarizer(
            openai_executer=openai_executer,
            is_debug=False)
        append_context_service = SlackConciergeInjector.create_append_context_service()
        client = ClientWrapper.get_instance()
        return AddWebclipUsecase(
            scrape_service=scrape_service,
            inbox_service=inbox_service,
            append_context_service=append_context_service,
            tag_create_service=tag_create_service,
            tag_analyzer=tag_analyzer,
            text_summarizer=text_summarizer,
            client=client,
        )

    @classmethod
    def create_inbox_service(cls: "Injector") -> InboxService:
        slack_client = WebClient()
        return InboxService(slack_client=slack_client)

    @classmethod
    def create_tag_create_service(cls: "Injector") -> TagCreateService:
        return TagCreateService()

    @classmethod
    def create_tag_analyzer(
            cls: "Injector",
            openai_executer: OpenaiExecuter,
            is_debug: bool|None=None) -> TagAnalyzer:
        return TagAnalyzer(
            client=openai_executer,
            logger=logger,
            is_debug=is_debug,
        )

    @classmethod
    def create_text_summarizer(
            cls: "Injector",
            openai_executer: OpenaiExecuter,
            is_debug: bool|None=None) -> TextSummarizer:
        return TextSummarizer(
            logger=logger,
            client=openai_executer,
            is_debug=is_debug,
        )

    @classmethod
    def __create_openai_executer(
        cls: "Injector",
        model: str|None=None,
        logger: Logger|None=None) -> TagAnalyzer:
        return OpenaiExecuter(model=model, logger=logger)
