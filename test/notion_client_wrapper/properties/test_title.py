import sys
from unittest import TestCase

from notion_client_wrapper.page.page_id import PageId

sys.path.append("notion_api")

# クラス名の一致をチェックするロジックがあるので、完全に合わせておく
from lotion.properties import Title


class TestTitle(TestCase):
    def test_シンプルなテキスト(self) -> None:
        input = "dummy"
        actual = Title.from_plain_text(text=input)

        # Then
        self.assertEqual(actual.text, input)

    def test_テキストとページメンションを合わせて利用(self) -> None:
        input = "dummy"
        page_id = PageId.dummy()
        page_title = "Mentioned Page"
        actual = Title.from_mentioned_page(mentioned_page_id=page_id, mentioned_page_title=page_title, prefix=input)

        # Then
        self.assertEqual(actual.text, "dummyMentioned Page")
