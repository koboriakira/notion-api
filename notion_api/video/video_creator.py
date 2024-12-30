from logging import Logger, getLogger

from lotion import Lotion

from common.infrastructure.default_scraper import DefaultScraper
from common.service.page_creator import PageCreator
from common.service.scrape_service.scrape_service import ScrapeService
from common.service.tag_creator import TagCreator
from notion_databases.video import Video, VideoName
from util.tag_analyzer import TagAnalyzer


class VideoCreator(PageCreator):
    def __init__(
        self,
        scrape_service: ScrapeService,
        tag_creator: TagCreator,
        tag_analyzer: TagAnalyzer,
        logger: Logger | None = None,
    ) -> None:
        self._scrape_service = scrape_service
        self._tag_creator = tag_creator
        self._tag_analyzer = tag_analyzer
        self._logger = logger or getLogger(__name__)
        self._lotion = Lotion.get_instance()

    def execute(
        self,
        url: str,
        title: str | None = None,
        cover: str | None = None,
        params: dict | None = None,
    ) -> Video:
        if title is None:
            msg = "title is required"
            raise ValueError(msg)

        info_message = f"{self.__class__} execute: url={url}, title={title}, cover={cover}"
        self._logger.info(info_message)

        video_title = VideoName.from_plain_text(title)
        video = self._lotion.find_page(Video, video_title)
        if video is not None:
            info_message = f"Video is already registered: {video.title.text}"
            self._logger.info(info_message)
            return video

        info_message = "Create a Video"
        self._logger.info(info_message)

        # カバー画像が指定されてなければ取得を試みる
        if cover is None:
            cover = self._scrape_service.execute(url=url).get_image_url()

        # タグを解析
        tags = self._tag_analyzer.handle(text=title)
        tag_page_id_list = self._tag_creator.execute(tag=tags)

        # Videoを生成
        video = Video.generate(
            title=title,
            url=url,
            cover=cover,
            tag_relation=tag_page_id_list,
        )

        return self._lotion.update(video)


if __name__ == "__main__":
    # python -m notion_api.video.service.video_creator
    from lotion import Lotion

    client = Lotion.get_instance()
    default_scraper = DefaultScraper()
    scrape_service = ScrapeService(scraper=default_scraper)
    suite = VideoCreator(
        scrape_service=scrape_service,
        tag_creator=TagCreator(),
        tag_analyzer=TagAnalyzer(),
    )
    suite.execute(
        url="https://www.youtube.com/watch?v=82KT4FNyNdY",
        title="火起こしモコピ | ヘアピンまみれ Hairpin Mamire",
    )
