from abc import ABCMeta, abstractmethod


class SlackConciergeAPI(metaclass=ABCMeta):
    @abstractmethod
    def append_context_block(self, channel: str, event_ts: str, context: dict) -> None:
        pass
