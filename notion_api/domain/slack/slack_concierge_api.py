from abc import ABCMeta, abstractmethod


class SlackConciergeAPI(metaclass=ABCMeta):
    @abstractmethod
    def append_context_block(self, data: dict) -> None:
        pass
