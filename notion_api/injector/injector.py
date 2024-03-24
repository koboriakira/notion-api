from slack_sdk.web import WebClient

from custom_logger import get_logger
from usecase.service.inbox_service import InboxService
from usecase.service.openai_executer import OpenaiExecuter
from usecase.service.tag_analyzer import TagAnalyzer
from usecase.service.tag_create_service import TagCreateService

logger = get_logger(__name__)

DEFAULT_GPT_MODEL = "gpt-3.5-turbo-1106"

class Injector:
    @staticmethod
    def create_inbox_service() -> InboxService:
        slack_client = WebClient()
        return InboxService(slack_client=slack_client)

    @staticmethod
    def create_tag_create_service() -> TagCreateService:
        return TagCreateService()

    @staticmethod
    def create_tag_analyzer(is_debug: bool|None=None) -> TagAnalyzer:
        openai_executer = OpenaiExecuter(model=DEFAULT_GPT_MODEL, logger=logger)
        return TagAnalyzer(
            client=openai_executer,
            logger=logger,
            is_debug=is_debug,
        )
