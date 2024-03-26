from common.infrastructure.default_scraper import DefaultScraper
from common.service.scrape_service.scrape_service import ScrapeService
from common.service.tweet.tweet_fetcher import TweetFetcher
from notion_api.common.infrastructure.twitter.lambda_twitter_api import LambdaTwitterApi


class CommonInjector:
    @staticmethod
    def get_scrape_service() -> ScrapeService:
        scraper = DefaultScraper()
        return ScrapeService(scraper=scraper)

    @staticmethod
    def get_tweet_fetcher() -> TweetFetcher:
        twitter_api = LambdaTwitterApi()
        return TweetFetcher(twitter_api=twitter_api)
