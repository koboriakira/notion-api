from lotion import Lotion

from common.infrastructure.default_scraper import DefaultScraper
from common.injector import CommonInjector
from common.service.scrape_service.scrape_service import ScrapeService
from custom_logger import get_logger
from util.tag_analyzer import TagAnalyzer
from video.service.video_creator import VideoCreator

logger = get_logger(__name__)
client = Lotion.get_instance()
scrape_service = CommonInjector.get_scrape_service()
tag_creator = CommonInjector.get_tag_creator()
tag_analyzer = TagAnalyzer()
scraper = DefaultScraper()
scrape_service = ScrapeService(scraper=scraper)


class VideoInjector:
    @classmethod
    def create_video_creator(cls) -> VideoCreator:
        return VideoCreator(
            scrape_service=scrape_service,
            tag_creator=tag_creator,
            tag_analyzer=tag_analyzer,
            logger=logger,
        )
