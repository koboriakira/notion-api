from unittest import TestCase

from notion_api.notion_client_wrapper.block.bulleted_list_item import BulletedlistItem
from notion_api.notion_client_wrapper.block.rich_text import RichText


class TestBulletedlistItem(TestCase):
    def test(self) -> None:
        # Given
        rich_text_foo = RichText.from_plain_text("foo")
        suite = BulletedlistItem.from_rich_text(rich_text_foo)

        # When
        # Then
        self.assertEqual("- foo", suite.to_slack_text())
