from abc import ABCMeta, abstractmethod

from zettlekasten.domain.zettlekasten import Zettlekasten


class ZettlekastenRepository(metaclass=ABCMeta):
    @abstractmethod
    def fetch_all(self) -> list[Zettlekasten]:
        pass

    @abstractmethod
    def search(
        self,
        is_tag_empty: bool | None = None,
        include_children: bool | None = None,
    ) -> list[Zettlekasten]:
        pass

    @abstractmethod
    def find_by_title(self, title: str) -> Zettlekasten | None:
        pass

    @abstractmethod
    def save(self, zettlekasten: Zettlekasten) -> Zettlekasten:
        pass
