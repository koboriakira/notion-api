from unittest import TestCase

from notion_api.lotion.base_page import BasePage


class TestBasePage(TestCase):
    def test_ページを作成する(self):
        # When
        actual = BasePage.create(properties=[], blocks=[])

        # Then
        self.assertEqual([], actual.properties.values)

    def test_タイトルとリンクをSlack形式で出力する(self):
        # isinstanceのためにパスを揃える
        import sys

        sys.path.append("notion_api")
        from lotion.properties import Title

        # Given
        base_page = BasePage.create(
            properties=[Title.from_plain_text(name="名前", text="タイトル")],
        )
        base_page.update_id_and_url(page_id="dummy-id", url="http://example.com")

        # When
        actual = base_page.title_for_slack()

        # Then
        self.assertEqual("<http://example.com|タイトル>", actual)
