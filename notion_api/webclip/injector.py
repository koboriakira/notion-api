from custom_logger import get_logger
from notion_client_wrapper.client_wrapper import ClientWrapper
from webclip.infrastructure.webclip_repository_impl import WebclipRepositoryImpl
from webclip.service.webclip_creator import WebclipCreator

logger = get_logger(__name__)

class Injector:
    @staticmethod
    def create_webclip_creator() -> WebclipCreator:
        client = ClientWrapper.get_instance()
        webclip_repository = WebclipRepositoryImpl(client=client, logger=logger)
        return WebclipCreator(webclip_repository=webclip_repository, logger=logger)
