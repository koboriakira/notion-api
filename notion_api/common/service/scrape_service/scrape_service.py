from common.infrastructure.default_scraper import DefaultScraper as Scraper
from common.service.scrape_service.response import Response


class ScrapeService:
    def __init__(self, scraper: Scraper) -> None:
        self._scraper = scraper

    def execute(self, url: str) -> Response:
        scraped_result = self._scraper.execute(url)
        return Response(
            not_formatted_text=scraped_result.not_formatted_text,
            formatted_text=scraped_result.formatted_text,
            ogp_tags=scraped_result.ogp_tags.values,
            other_meta_tags=scraped_result.other_meta_tags.values,
        )

if __name__ == "__main__":
    # python -m notion_api.common.service.scrape_service.scrape_service
    service = ScrapeService(scraper=Scraper())
    result = service.execute("https://www.youtube.com/watch?v=82KT4FNyNdY")
    print(result.get_image_url())
