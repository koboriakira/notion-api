from logging import Logger, getLogger

from notion_client_wrapper.properties.tag_relation import TagRelation
from webclip.domain.webclip import Webclip
from webclip.infrastructure.webclip_repository_impl import WebclipRepositoryImpl


class WebclipCreator:
    def __init__(
            self,
            webclip_repository: WebclipRepositoryImpl,
            logger: Logger | None = None,
            ) -> None:
        self._webclip_repository = webclip_repository
        self._logger = logger or getLogger(__name__)

    def execute(  # noqa: PLR0913
            self,
            url: str,
            title: str,
            cover: str | None = None,
            slack_channel: str | None = None,
            slack_thread_ts: str | None = None,
            ) -> dict:
        info_message = f"{self.__class__} execute: url={url}, title={title}, cover={cover}, slack_channel={slack_channel}, slack_thread_ts={slack_thread_ts}"
        self._logger.info(info_message)

        webclip = self._webclip_repository.find_by_title(title=title)
        if webclip is not None:
            info_message = f"Webclip is already registered: {webclip.get_title_text()}"
            self._logger.info(info_message)
            return {
                "id": webclip.id,
                "url": webclip.url,
            }

        info_message = "Create a Webclip"
        self._logger.info(info_message)

        tag_relation = TagRelation.empty() # FIXME: あとで埋める

        webclip = Webclip.create(
            title=title,
            url=url,
            tag_relation=tag_relation,
            cover=cover,
            summary=None, # FIXME: あとでいれる
        )
        webclip = self._webclip_repository.save(webclip=webclip)
        return {
            "id": webclip.id,
            "url": webclip.url,
        }


if __name__ == "__main__":
    # python -m notion_api.webclip.service.webclip_creator
    from webclip.injector import Injector
    service = Injector.create_webclip_creator()
    service.execute(
        url="https://twoucan.com/profile/mapico_",
        title="まぴこ (@mapico_) さんのイラスト・マンガ作品まとめ (82 件) - Twoucan",
    )
