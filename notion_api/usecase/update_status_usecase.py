from custom_logger import get_logger
from notion_client_wrapper.client_wrapper import ClientWrapper

logger = get_logger(__name__)


class UpdateStatusUsecase:
    def __init__(self) -> None:
        self.client = ClientWrapper.get_instance()

    def execute(
        self,
        page_id: str,
        value: str,
    ) -> dict:
        raise NotImplementedError
