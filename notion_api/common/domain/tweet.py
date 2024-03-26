from dataclasses import dataclass


@dataclass
class Tweet:
    tweet_id: str
    url: str
    media_urls: list[str]
