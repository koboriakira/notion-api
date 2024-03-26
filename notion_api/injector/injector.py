import os
from logging import Logger

from slack_sdk.web import WebClient

from custom_logger import get_logger
from notion_api.notion_client_wrapper.client_wrapper import ClientWrapper
from slack_concierge.injector import SlackConciergeInjector
from usecase.add_webclip_usecase import AddWebclipUsecase
from usecase.service.inbox_service import InboxService
from usecase.service.tag_analyzer import TagAnalyzer
from usecase.service.tag_create_service import TagCreateService
from usecase.service.text_summarizer import TextSummarizer
from util.openai_executer import OpenaiExecuter
from webclip.injector import WebclipInjector

logger = get_logger(__name__)

DEFAULT_GPT_MODEL = "gpt-3.5-turbo-1106"

client = ClientWrapper.get_instance()
slack_bot_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

class Injector:
    @classmethod
    def create_add_webclip_usecase(cls: "Injector") -> AddWebclipUsecase:
        webclip_creator = WebclipInjector.create_webclip_creator()
        inbox_service = cls.create_inbox_service()
        append_context_service = SlackConciergeInjector.create_append_context_service()
        return AddWebclipUsecase(
            webclip_creator=webclip_creator,
            inbox_service=inbox_service,
            append_context_service=append_context_service,
            logger=logger,
        )

    @classmethod
    def create_inbox_service(cls: "Injector") -> InboxService:
        return InboxService(slack_client=slack_bot_client, client=client)

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
