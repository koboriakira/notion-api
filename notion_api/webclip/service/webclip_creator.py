from logging import Logger, getLogger

from lotion import Lotion

from common.service.page_creator import PageCreator
from notion_databases.webclip import Webclip
from webclip.service.webclip_generator import WebclipGeneratorRule


class WebclipCreator(PageCreator):
    def __init__(
        self,
        webclip_generator_rule: WebclipGeneratorRule,
        logger: Logger | None = None,
    ) -> None:
        self._webclip_generator_rule = webclip_generator_rule
        self._logger = logger or getLogger(__name__)
        self._lotion = Lotion.get_instance()

    def execute(
        self,
        url: str,
        title: str,
        cover: str | None = None,
        params: dict | None = None,
    ) -> Webclip:
        info_message = f"{self.__class__} execute: url={url}, title={title}, cover={cover}"
        self._logger.info(info_message)

        webclip = self._find_webclip(title=title)
        if webclip is not None:
            return webclip

        # Webclipを生成
        webclip_generator = self._webclip_generator_rule.get_generator(url=url)
        webclip = webclip_generator.execute(
            url=url,
            title=title,
            cover=cover,
        )
        return self._lotion.update(webclip)

    def _find_webclip(self, title: str) -> Webclip | None:
        webclip = self._lotion.find_page_by_title(
            database_id=Webclip.DATABASE_ID,
            title=title,
            title_key_name="名前",
            cls=Webclip,
        )
        if webclip is not None:
            info_message = f"Webclip is already registered: {webclip.get_title_text()}"
            self._logger.info(info_message)
            return webclip

        info_message = "Create a Webclip"
        self._logger.info(info_message)
        return None


if __name__ == "__main__":
    # python -m notion_api.webclip.service.webclip_creator
    from webclip.injector import WebclipInjector

    service = WebclipInjector.create_webclip_creator()
    service.execute(
        url="https://hobby.dengeki.com/news/2222026/",
        title="『爆走兄弟レッツ＆ゴー!!』のミニ四駆がミニカー化！マグナムセイバーなどの「トミカプレミアムunlimited」がAmazonで予約受付中!! | 電撃ホビーウェブ",
    )
