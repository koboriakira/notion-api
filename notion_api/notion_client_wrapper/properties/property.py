from abc import ABCMeta, abstractmethod
from typing import Optional, Any

class Property(metaclass=ABCMeta):
    id: Optional[str]
    name: str
    type: str

    @abstractmethod
    def __dict__(self):
        pass
