from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.properties import Status
from domain.status import StatusEnum
from custom_logger import get_logger


logger = get_logger(__name__)

class UpdateStatusUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()

    def execute(self,
                page_id: str,
                value: str,
                ) -> dict:
        status_enum = StatusEnum.get_status(value=value)
        status = Status.from_status_name(name="ステータス", status_name=status_enum.value)
        self.client.update_page(
            page_id=page_id,
            properties=[status]
        )
