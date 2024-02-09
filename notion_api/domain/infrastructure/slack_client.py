from abc import ABCMeta, abstractmethod
from typing import Optional

class SlackClient(metaclass=ABCMeta):

    @abstractmethod
    def send_message(self, channel: str, text: str, thread_ts: Optional[str] = None) -> dict:
        pass

    @abstractmethod
    def update_message(self, channel: str, ts: str, text: str, blocks: Optional[list] = None) -> dict:
        pass
