from logging import Logger
from unittest import TestCase
from unittest.mock import Mock

from notion_api.common.service.tag_creator.tag_creator import TagCreator
from notion_api.common.service.tweet.tweet_fetcher import TweetFetcher
from notion_api.util.tag_analyzer import TagAnalyzer
from parameterized import parameterized

from webclip.webclip_generator import TwitterWebclipGenerator


class TestTwitterWebclipGenerator(TestCase):
    def setUp(self):
        tweet_fetcher = Mock(spec=TweetFetcher)
        tag_creator = Mock(spec=TagCreator)
        tag_analyzer = Mock(spec=TagAnalyzer)
        logger = Mock(spec=Logger)
        self.client = TwitterWebclipGenerator(
            tweet_fetcher=tweet_fetcher,
            tag_creator=tag_creator,
            tag_analyzer=tag_analyzer,
            logger=logger,
        )

    @parameterized.expand(
        [
            ("https://twitter.com/harajuku_tjpw/status/1772269440396333105", "1772269440396333105"),
            ("https://twitter.com/harajuku_tjpw/status/1772269440396333105/photo/1", "1772269440396333105"),
        ]
    )
    def test_extract_twitter_id(self, input, expected):
        self.assertEqual(self.client._extract_tweet_id(input), expected)
