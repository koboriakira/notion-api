from logging import Logger

from slack_sdk.web import WebClient

from custom_logger import get_logger
from usecase.service.inbox_service import InboxService
from usecase.service.openai_executer import OpenaiExecuter
from usecase.service.tag_analyzer import TagAnalyzer
from usecase.service.tag_create_service import TagCreateService
from usecase.service.text_summarizer import TextSummarizer

logger = get_logger(__name__)

DEFAULT_GPT_MODEL = "gpt-3.5-turbo-1106"

class Injector:
    @classmethod
    def create_inbox_service(cls: "Injector") -> InboxService:
        slack_client = WebClient()
        return InboxService(slack_client=slack_client)

    @classmethod
    def create_tag_create_service(cls: "Injector") -> TagCreateService:
        return TagCreateService()

    @classmethod
    def create_tag_analyzer(cls: "Injector", is_debug: bool|None=None) -> TagAnalyzer:
        openai_executer = cls.__create_openai_executer(model=DEFAULT_GPT_MODEL, logger=logger)
        return TagAnalyzer(
            client=openai_executer,
            logger=logger,
            is_debug=is_debug,
        )

    @classmethod
    def create_text_summarizer(cls: "Injector", is_debug: bool|None=None) -> TextSummarizer:
        openai_executer = cls.__create_openai_executer(model=DEFAULT_GPT_MODEL, logger=logger)
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
