import os
from logging import Logger

from lotion import Lotion
from slack_sdk.web import WebClient

from book.book_api import BookApi
from common.service.tag_creator.tag_creator import TagCreator
from custom_logger import get_logger
from daily_log.daily_log_repository_impl import DailyLogRepositoryImpl
from external_calendar.infrastructure.google_calendar_api import GoogleCalendarApi
from external_calendar.service.external_calendar_service import ExternalCalendarService
from injector.page_creator_factory import PageCreatorFactory
from project.project_repository_impl import ProjectRepositoryImpl
from recipe.recipe_creator import RecipeCreator
from slack_concierge.injector import SlackConciergeInjector
from task.task_repository_impl import TaskRepositoryImpl
from usecase.account_book.add_account_book_usecase import AddAccountBookUsecase
from usecase.add_book_usecase import AddBookUsecase
from usecase.collect_updated_pages_usecase import CollectUpdatedPagesUsecase
from usecase.create_page_use_case import CreatePageUseCase
from usecase.create_routine_task_use_case import CreateRoutineTaskUseCase
from usecase.project.convert_to_project_usecase import ConvertToProjectUsecase
from usecase.project.create_project_service import CreateProjectService
from usecase.recipe.add_recipe_use_case import AddRecipeUseCase
from usecase.service.inbox_service import InboxService
from usecase.service.text_summarizer import TextSummarizer
from usecase.task.abort_task_usecase import AbortTaskUsecase
from usecase.task.sync_external_calendar_usecase import SyncExternalCalendarUsecase
from usecase.task.task_util_service import TaskUtilService
from usecase.zettlekasten.create_tag_to_zettlekasten_use_case import CreateTagToZettlekastenUseCase
from util.openai_executer import OpenaiExecuter
from util.tag_analyzer import TagAnalyzer

logger = get_logger(__name__)


client = Lotion.get_instance()
openai_executer = OpenaiExecuter(logger=logger)
slack_bot_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])


class Injector:
    @staticmethod
    def get_create_tag_to_zettlekasten_use_case() -> CreateTagToZettlekastenUseCase:
        tag_analyzer = TagAnalyzer(
            client=openai_executer,
            logger=logger,
        )
        tag_creator = TagCreator(
            client=client,
        )
        return CreateTagToZettlekastenUseCase(
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
        daily_log_repository = DailyLogRepositoryImpl(client=client)
        return CollectUpdatedPagesUsecase(
            task_repository=task_repository,
            daily_log_repository=daily_log_repository,
            is_debug=is_debug,
        )

    @staticmethod
    def create_add_recipe_use_case(
        logger: Logger | None = None,
    ) -> AddRecipeUseCase:
        logger = logger or get_logger(__name__)
        recipe_creator = RecipeCreator(openai_executer=openai_executer, logger=logger)
        return AddRecipeUseCase(
            recipe_creator=recipe_creator,
            slack_client=slack_bot_client,
            logger=logger,
        )

    @staticmethod
    def create_add_account_book_use_case(logger: Logger | None = None) -> AddAccountBookUsecase:
        return AddAccountBookUsecase(lotion=Lotion.get_instance())

    @staticmethod
    def create_routine_task_use_case() -> CreateRoutineTaskUseCase:
        task_repository = TaskRepositoryImpl()
        return CreateRoutineTaskUseCase(task_repository=task_repository)

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
    def add_book_usecase(book_api: BookApi) -> AddBookUsecase:
        return AddBookUsecase(book_api=book_api)

    @staticmethod
    def abort_task_usecase() -> AbortTaskUsecase:
        task_repository = TaskRepositoryImpl()
        return AbortTaskUsecase(task_repository=task_repository)

    @staticmethod
    def create_project_service() -> CreateProjectService:
        return CreateProjectService(lotion=client)

    @staticmethod
    def convert_to_project_usecase() -> ConvertToProjectUsecase:
        project_repository = ProjectRepositoryImpl()
        return ConvertToProjectUsecase(
            lotion=Lotion.get_instance(),
            project_repository=project_repository,
        )

    @staticmethod
    def task_util_serivce() -> TaskUtilService:
        return TaskUtilService()
