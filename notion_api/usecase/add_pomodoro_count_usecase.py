from notion_client_wrapper.client_wrapper import ClientWrapper
from custom_logger import get_logger

logger = get_logger(__name__)

class AddPomodoroCountUsecase:
    def __init__(self):
        self.client = ClientWrapper.get_instance()

    def execute(self, page_id: str) -> dict:
        page = self.client.retrieve_page(page_id=page_id)
        pomodoro_count = page.get_number(name="ポモドーロカウンター").add(1)
        self.client.update_page(
            page_id=page_id,
            properties=[pomodoro_count]
        )
