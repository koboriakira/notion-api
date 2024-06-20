from abc import ABCMeta, abstractmethod

from notion_client_wrapper.base_page import BasePage


class PageCreator(metaclass=ABCMeta):
    @abstractmethod
    def execute(
        self,
        url: str,
        title: str | None = None,
        cover: str | None = None,
        params: dict | None = None,
    ) -> BasePage:
        pass


class NotImplementPageCreator(PageCreator):
    def execute(
        self,
        url: str,
        title: str | None = None,  # noqa: ARG002
        cover: str | None = None,  # noqa: ARG002
        params: dict | None = None,  # noqa: ARG002
    ) -> BasePage:
        msg = f"The page creator is not implemented. url: {url}"
        raise NotImplementedError(msg)
