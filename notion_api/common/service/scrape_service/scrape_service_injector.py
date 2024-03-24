from common.infrastructure.default_scraper import DefaultScraper
from common.service.scrape_service.scrape_service import ScrapeService


class ScrapeServiceInjector:
    @staticmethod
    def get_instance() -> ScrapeService:
        scraper = DefaultScraper()
        return ScrapeService(scraper=scraper)
