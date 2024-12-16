from lotion import Lotion
from custom_logger import get_logger

logger = get_logger(__name__)

class AddPomodoroCountUsecase:
    def __init__(self):
        self.client = Lotion.get_instance()

    def execute(self, page_id: str) -> dict:
        page = self.client.retrieve_page(page_id=page_id)
        pomodoro_count = page.get_number(name="ポモドーロカウンター").add(1)
        self.client.update_page(
            page_id=page_id,
            properties=[pomodoro_count]
        )
