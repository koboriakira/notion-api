from abc import ABCMeta, abstractmethod

from notion_client_wrapper.base_page import BasePage


class PageCreator(metaclass=ABCMeta):
    @abstractmethod
    def execute(
            self,
            url: str,
            title: str | None = None,
            cover: str | None = None,
            ) -> BasePage:
        pass
