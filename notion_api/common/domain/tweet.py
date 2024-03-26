from dataclasses import dataclass


@dataclass
class Tweet:
    tweet_id: str
    text: str
    user_name: str
    url: str
    media_urls: list[str]
