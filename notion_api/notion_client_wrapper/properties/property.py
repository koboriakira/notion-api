from abc import ABCMeta, abstractmethod


class Property(metaclass=ABCMeta):
    id: str | None
    name: str
    type: str

    @abstractmethod
    def __dict__(self):
        pass

    # @abstractmethod
    # def value_for_filter(self) -> str:
    #     pass
