from lotion import Lotion

from custom_logger import get_logger

logger = get_logger(__name__)


class AppendFeelingUsecase:
    def __init__(self):
        self.client = Lotion.get_instance()

    def execute(
        self,
        page_id: str,
        value: str,
    ) -> dict:
        logger.info("AppendFeelingUsecase start")
        page = self.client.retrieve_page(page_id=page_id)
        feeling = page.get_text(name="気持ち").append_text(text=value)
        return self.client.update_page(
            page_id=page_id,
            properties=[feeling],
        )
