from common.domain.tweet import Tweet
from common.infrastructure.twitter.lambda_twitter_api import LambdaTwitterApi as TwitterApi


class TweetFetcher:
    def __init__(self, twitter_api: TwitterApi) -> None:
        self._twitter_api = twitter_api

    def fetch(self, tweet_id: str) -> Tweet:
        tweet = self._twitter_api.get_tweet(tweet_id)
        return tweet.to_entity()
