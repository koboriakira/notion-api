from custom_logger import get_logger
from notion_client_wrapper.client_wrapper import ClientWrapper
from usecase.service.base_page_converter import BasePageConverter

logger = get_logger(__name__)

class FindTaskUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()

    def execute(self,
                id: str,
                ) -> dict:
        page = self.client.retrieve_page(page_id=id)
        return BasePageConverter.to_task(page=page)
