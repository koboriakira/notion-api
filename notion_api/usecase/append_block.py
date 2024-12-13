from lotion import Lotion
from notion_client_wrapper.block import Paragraph
from custom_logger import get_logger


logger = get_logger(__name__)

class AppendBlockUsecase:
    def __init__(self):
        self.client = Lotion.get_instance()

    def append_text(self,
                    page_id: str,
                    value: str,
                    ) -> dict:
        paragrah = Paragraph.from_plain_text(value)
        self.client.append_block(block_id=page_id, block=paragrah)
