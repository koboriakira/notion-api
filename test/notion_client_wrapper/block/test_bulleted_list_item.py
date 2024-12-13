from unittest import TestCase

from lotion.block import BulletedlistItem
from lotion.block.rich_text import RichText


class TestBulletedlistItem(TestCase):
    def test(self) -> None:
        # Given
        rich_text_foo = RichText.from_plain_text("foo")
        suite = BulletedlistItem.from_rich_text(rich_text_foo)

        # When
        # Then
        self.assertEqual("- foo", suite.to_slack_text())
