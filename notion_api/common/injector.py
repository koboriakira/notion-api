from common.infrastructure.default_scraper import DefaultScraper
from common.service.scrape_service.scrape_service import ScrapeService


class CommonInjector:
    @staticmethod
    def get_scrape_service() -> ScrapeService:
        scraper = DefaultScraper()
        return ScrapeService(scraper=scraper)
