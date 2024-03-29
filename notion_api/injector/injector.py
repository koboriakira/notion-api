import os
from logging import Logger

from slack_sdk.web import WebClient

from common.service.tag_creator.tag_creator import TagCreator
from custom_logger import get_logger
from injector.page_creator_factory import PageCreatorFactory
from notion_client_wrapper.client_wrapper import ClientWrapper
from slack_concierge.injector import SlackConciergeInjector
from usecase.add_webclip_usecase import AddWebclipUsecase
from usecase.create_page_use_case import CreatePageUseCase
from usecase.service.inbox_service import InboxService
from usecase.service.tag_analyzer import TagAnalyzer
from usecase.service.tag_create_service import TagCreateService
from usecase.service.text_summarizer import TextSummarizer
from usecase.zettlekasten.create_tag_to_zettlekasten_use_case import CreateTagToZettlekastenUseCase
from util.openai_executer import OpenaiExecuter
from webclip.injector import WebclipInjector
from zettlekasten.infrastructure.zettlekasten_repository_impl import ZettlekastenRepositoryImpl

logger = get_logger(__name__)

DEFAULT_GPT_MODEL = "gpt-3.5-turbo-1106"

client = ClientWrapper.get_instance()
openai_executer = OpenaiExecuter(
    model=OpenaiExecuter.DEFAULT_GPT_MODEL,
    logger=logger)
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
    def get_create_tag_to_zettlekasten_use_case(cls: "Injector") -> CreateTagToZettlekastenUseCase:
        zettlekasten_repository = ZettlekastenRepositoryImpl(
            client=client,
            logger=logger,
        )
        tag_analyzer = TagAnalyzer(
            client=openai_executer,
            logger=logger,
        )
        tag_creator = TagCreator(
            client=client,
        )
        return CreateTagToZettlekastenUseCase(
            zettlekasten_repository=zettlekasten_repository,
            tag_analyzer=tag_analyzer,
            tag_creator=tag_creator,
            logger=logger,
        )

    @classmethod
    def create_inbox_service(cls: "Injector") -> InboxService:
        return InboxService(slack_client=slack_bot_client, client=client)

    @classmethod
    def create_tag_create_service(cls: "Injector") -> TagCreateService:
        return TagCreateService()

    @classmethod
    def create_page_use_case(cls: "Injector") -> CreatePageUseCase:
        page_creator_factory = PageCreatorFactory.generate_rule(logger=logger)
        inbox_service = cls.create_inbox_service()
        append_context_service = SlackConciergeInjector.create_append_context_service()
        return CreatePageUseCase(
            page_creator_factory=page_creator_factory,
            inbox_service=inbox_service,
            append_context_service=append_context_service,
            logger=logger,
        )

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
