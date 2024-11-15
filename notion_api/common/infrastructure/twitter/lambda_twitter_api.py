import json
import os
from datetime import datetime, timedelta

import requests

import custom_logger
from common.infrastructure.twitter.tweet_response import TweetModel
from util.datetime import jst_now


class TwitterApiError(Exception):
    pass


class LambdaTwitterApi:
    def __init__(self) -> None:
        self.domain = os.environ["LAMBDA_TWITTER_API_DOMAIN"]
        self._logger = custom_logger.get_logger(__name__)

    def get_tweet(self, tweet_id: str) -> TweetModel:
        path = f"/tweet/{tweet_id}"
        response = self.__get(path=path)
        return TweetModel.from_dict(response["data"])

    def get_user_tweets(
        self,
        user_screen_name: str,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[TweetModel]:
        path = f"/user/{user_screen_name}/tweets/"
        params = {
            "start": start_datetime.isoformat() if start_datetime else None,
            "end": end_datetime.isoformat() if end_datetime else None,
        }
        response = self.__get(path=path, params=params)
        self._logger.debug(f"response: {response['data']}")
        response_data: list[dict] = response["data"]
        return [TweetModel.from_dict(tweet) for tweet in response_data]

    def __get(self, path: str, params: dict | None = None) -> dict:
        url = f"{self.domain}{path}"
        response = requests.get(url, params=params, timeout=180)
        if response.status_code != 200:
            data_str = json.dumps(params, ensure_ascii=False)
            error_messsage = f"Failed to get to {url}. status_code: {response.status_code}, response: {response.text}, params: {data_str}"
            raise TwitterApiError(error_messsage)
        return response.json()


if __name__ == "__main__":
    # python -m notion_api.common.infrastructure.twitter.lambda_twitter_api
    api = LambdaTwitterApi()
    # tweet = api.get_tweet("1772269440396333105")
    # print(tweet.to_entity())
    now = jst_now()
    tweets = api.get_user_tweets(
        user_screen_name="kobori_akira_pw",
        start_datetime=now - timedelta(hours=7),
        end_datetime=now,
        )
    print(len(tweets))
    print(tweets[0].to_entity())
