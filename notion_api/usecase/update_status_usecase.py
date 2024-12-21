from lotion import Lotion

from custom_logger import get_logger

logger = get_logger(__name__)


class UpdateStatusUsecase:
    def __init__(self) -> None:
        self.client = Lotion.get_instance()

    def execute(
        self,
        page_id: str,
        value: str,
    ) -> dict:
        raise NotImplementedError
