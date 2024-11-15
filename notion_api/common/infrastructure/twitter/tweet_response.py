from dataclasses import dataclass, field
from datetime import datetime

from common.domain.tweet import Tweet


@dataclass
class UserModel:
    id: str
    name: str
    screen_name: str


@dataclass
class MediumModel:
    url: str
    alt_text: str


@dataclass
class TweetModel:
    id: str
    text: str
    url: str
    created_at: datetime
    user: UserModel
    embed_tweet_html: str
    media: list[MediumModel] | None = field(default=None)


    def to_entity(self) -> Tweet:
        return Tweet(
            tweet_id=self.id,
            text=self.text,
            user_name=self.user.name,
            url=self.url,
            media_urls=[medium.url for medium in self.media] if self.media is not None else [],
        )

    @staticmethod
    def from_dict(tweet_data: dict) -> "TweetModel":
        user_data = tweet_data["user"]
        user = UserModel(
            id=user_data["id"],
            name=user_data["name"],
            screen_name=user_data["screen_name"],
        )
        media = None
        if "media" in tweet_data and tweet_data["media"] is not None:
            media = [
                MediumModel(
                    url=medium["url"],
                    alt_text=medium["alt_text"],
                )
                for medium in tweet_data["media"]
            ]
        return TweetModel(
            id=tweet_data["id"],
            text=tweet_data["text"],
            url=tweet_data["url"],
            created_at=datetime.fromisoformat(tweet_data["created_at"]),
            user=user,
            embed_tweet_html=tweet_data["embed_tweet_html"],
            media=media,
        )
