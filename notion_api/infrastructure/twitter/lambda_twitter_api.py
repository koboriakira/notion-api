import json
import os

import requests

from notion_api.infrastructure.twitter.tweet_response import TweetResponse


class TwitterApiError(Exception):
    pass

# domain層に同名のクラスをつくったら、LambdaTwitterApiにリネームする
class TwitterApi:
    def __init__(self) -> None:
        self.domain = os.environ["LAMBDA_TWITTER_API_DOMAIN"]

    def get_tweet(self, tweet_id: str) -> TweetResponse:
        path = f"/tweet/{tweet_id}"
        response = self.__get(path=path)
        return TweetResponse.from_dict(response)

    def __get(self, path: str, params: dict|None = None) -> None:
        url = f"{self.domain}{path}"
        response = requests.get(url, params=params, timeout=30)
        if response.status_code != 200:
            data_str = json.dumps(params, ensure_ascii=False)
            error_messsage = f"Failed to get to {url}. status_code: {response.status_code}, response: {response.text}, params: {data_str}"
            raise TwitterApiError(error_messsage)
        return response.json()


if __name__ == "__main__":
    # python -m notion_api.infrastructure.twitter.lambda_twitter_api
    api = TwitterApi()
    tweet = api.get_tweet("1772383862393348494")
    print(tweet)
