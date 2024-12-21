import os
from logging import Logger

from lotion import Lotion
from slack_sdk.web import WebClient

from account_book.infrastructure.repository_impl import RepositoryImpl
from book.infrastructure.book_repository_impl import BookRepositoryImpl
from common.service.tag_creator.tag_creator import TagCreator
from custom_logger import get_logger
from daily_log.infrastructure.daily_log_repository_impl import DailyLogRepositoryImpl
from external_calendar.infrastructure.google_calendar_api import GoogleCalendarApi
from external_calendar.service.external_calendar_service import ExternalCalendarService
from infrastructure.book.google_book_api import GoogleBookApi
from injector.page_creator_factory import PageCreatorFactory
from music.infrastructure.song_repository_impl import SongRepositoryImpl
from recipe.infrastructure.recipe_repository_impl import RecipeRepositoryImpl
from recipe.service.recipe_creator import RecipeCreator
from slack_concierge.injector import SlackConciergeInjector
from task.infrastructure.routine_repository_impl import RoutineRepositoryImpl
from task.infrastructure.task_repository_impl import TaskRepositoryImpl
from usecase.account_book.add_account_book_usecase import AddAccountBookUsecase
from usecase.add_book_usecase import AddBookUsecase
from usecase.collect_updated_pages_usecase import CollectUpdatedPagesUsecase
from usecase.create_page_use_case import CreatePageUseCase
from usecase.create_routine_task_use_case import CreateRoutineTaskUseCase
from usecase.recipe.add_recipe_use_case import AddRecipeUseCase
from usecase.service.inbox_service import InboxService
from usecase.service.text_summarizer import TextSummarizer
from usecase.task.sync_external_calendar_usecase import SyncExternalCalendarUsecase
from usecase.zettlekasten.create_tag_to_zettlekasten_use_case import CreateTagToZettlekastenUseCase
from util.openai_executer import OpenaiExecuter
from util.tag_analyzer import TagAnalyzer
from video.infrastructure.video_repository_impl import VideoRepositoryImpl
from webclip.infrastructure.webclip_repository_impl import WebclipRepositoryImpl
from zettlekasten.infrastructure.zettlekasten_repository_impl import ZettlekastenRepositoryImpl

logger = get_logger(__name__)


client = Lotion.get_instance()
openai_executer = OpenaiExecuter(logger=logger)
slack_bot_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
book_repository = BookRepositoryImpl(
    client=client,
    logger=logger,
)


class Injector:
    @staticmethod
    def get_create_tag_to_zettlekasten_use_case() -> CreateTagToZettlekastenUseCase:
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

    @staticmethod
    def create_inbox_service() -> InboxService:
        return InboxService(slack_client=slack_bot_client, client=client)

    @staticmethod
    def create_page_use_case() -> CreatePageUseCase:
        page_creator_factory = PageCreatorFactory.generate_rule(logger=logger)
        inbox_service = Injector.create_inbox_service()
        append_context_service = SlackConciergeInjector.create_append_context_service()
        return CreatePageUseCase(
            page_creator_factory=page_creator_factory,
            inbox_service=inbox_service,
            append_context_service=append_context_service,
            logger=logger,
        )

    @staticmethod
    def create_tag_analyzer(
        openai_executer: OpenaiExecuter,
        is_debug: bool | None = None,
    ) -> TagAnalyzer:
        return TagAnalyzer(
            client=openai_executer,
            logger=logger,
            is_debug=is_debug,
        )

    @staticmethod
    def create_text_summarizer(
        openai_executer: OpenaiExecuter,
        is_debug: bool | None = None,
    ) -> TextSummarizer:
        return TextSummarizer(
            logger=logger,
            client=openai_executer,
            is_debug=is_debug,
        )

    @staticmethod
    def create_collect_updated_pages_usecase(
        is_debug: bool | None = None,
    ) -> CollectUpdatedPagesUsecase:
        task_repository = TaskRepositoryImpl(notion_client_wrapper=client)
        song_repository = SongRepositoryImpl(client=client)
        daily_log_repository = DailyLogRepositoryImpl(client=client)
        webclip_repository = WebclipRepositoryImpl(client=client)
        video_repository = VideoRepositoryImpl(client=client)
        return CollectUpdatedPagesUsecase(
            task_repository=task_repository,
            song_repository=song_repository,
            daily_log_repository=daily_log_repository,
            webclip_repository=webclip_repository,
            video_repository=video_repository,
            is_debug=is_debug,
        )

    @staticmethod
    def create_add_recipe_use_case(
        logger: Logger | None = None,
    ) -> AddRecipeUseCase:
        logger = logger or get_logger(__name__)
        recipe_creator = RecipeCreator(openai_executer=openai_executer, logger=logger)
        recipe_repository = RecipeRepositoryImpl(client=client, logger=logger)
        return AddRecipeUseCase(
            recipe_creator=recipe_creator,
            recipe_repository=recipe_repository,
            slack_client=slack_bot_client,
            logger=logger,
        )

    @staticmethod
    def create_add_account_book_use_case(logger: Logger | None = None) -> AddAccountBookUsecase:
        logger = logger or get_logger(__name__)
        repository = RepositoryImpl(client=client, logger=logger)
        return AddAccountBookUsecase(account_book_repository=repository)

    @staticmethod
    def create_routine_task_use_case() -> CreateRoutineTaskUseCase:
        task_repository = TaskRepositoryImpl()
        routine_repository = RoutineRepositoryImpl()
        return CreateRoutineTaskUseCase(task_repository=task_repository, routine_repository=routine_repository)

    @staticmethod
    def sync_external_calendar_usecase() -> SyncExternalCalendarUsecase:
        external_calendar_service = ExternalCalendarService(
            api=GoogleCalendarApi(),
        )
        return SyncExternalCalendarUsecase(
            task_repository=TaskRepositoryImpl(),
            external_calendar_service=external_calendar_service,
        )

    @staticmethod
    def add_book_usecase() -> AddBookUsecase:
        book_api = GoogleBookApi()
        return AddBookUsecase(book_api=book_api, book_repository=book_repository)
