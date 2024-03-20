from unittest import TestCase

from notion_api.notion_client_wrapper.base_page import BasePage


class TestBasePage(TestCase):
    def test_ページを作成する(self):
        # When
        actual = BasePage.create(properties=[], blocks=[])

        # Then
        self.assertEqual([], actual.properties.values)
