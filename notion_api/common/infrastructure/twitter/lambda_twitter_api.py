import json
import os
from datetime import datetime

import requests

from common.infrastructure.twitter.tweet_response import TweetResponse


class TwitterApiError(Exception):
    pass


class LambdaTwitterApi:
    def __init__(self) -> None:
        self.domain = os.environ["LAMBDA_TWITTER_API_DOMAIN"]

    def get_tweet(self, tweet_id: str) -> TweetResponse:
        path = f"/tweet/{tweet_id}"
        response = self.__get(path=path)
        return TweetResponse.from_dict(response)

    def get_user_tweets(
        self,
        user_screen_name: str,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[TweetResponse]:
        path = f"/user/{user_screen_name}/tweets/"
        response = self.__get(path=path)
        return [TweetResponse.from_dict(tweet) for tweet in response]

    def __get(self, path: str, params: dict | None = None) -> None:
        url = f"{self.domain}{path}"
        response = requests.get(url, params=params, timeout=30)
        if response.status_code != 200:
            data_str = json.dumps(params, ensure_ascii=False)
            error_messsage = f"Failed to get to {url}. status_code: {response.status_code}, response: {response.text}, params: {data_str}"
            raise TwitterApiError(error_messsage)
        return response.json()


if __name__ == "__main__":
    # python -m notion_api.common.infrastructure.twitter.lambda_twitter_api
    api = LambdaTwitterApi()
    # tweet = api.get_tweet("1772383862393348494")
    # print(tweet.to_entity())
    # tweets = api.get_user_tweets(user_screen_name="kobori_akira_pw")
    # print(tweets[0].to_entity())
