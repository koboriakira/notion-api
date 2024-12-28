from lotion import Lotion

from common.infrastructure.default_scraper import DefaultScraper
from common.infrastructure.twitter.lambda_twitter_api import LambdaTwitterApi
from common.service.scrape_service.scrape_service import ScrapeService
from common.service.tag_creator.tag_creator import TagCreator
from common.service.tweet.tweet_fetcher import TweetFetcher

client = Lotion.get_instance()


class CommonInjector:
    @staticmethod
    def get_scrape_service() -> ScrapeService:
        scraper = DefaultScraper()
        return ScrapeService(scraper=scraper)

    @staticmethod
    def get_tweet_fetcher() -> TweetFetcher:
        twitter_api = LambdaTwitterApi()
        return TweetFetcher(twitter_api=twitter_api)

    @staticmethod
    def get_tag_creator() -> TagCreator:
        return TagCreator(client=client)
