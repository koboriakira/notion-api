from unittest import TestCase

import pytest

from notion_client_wrapper.client_wrapper import ClientWrapper
from shopping.infrastructure.repository_impl import ShoppingRepositoryImpl


class TestShoppingRepositoryImpl(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    @pytest.mark.use_genuine_api()
    def test_すべての買い物リストを取得できる(self):
        # Given
        real_suite = ShoppingRepositoryImpl(client=ClientWrapper.get_instance())

        # When
        actual = real_suite.fetch_all()

        # Then
        self.assertTrue(len(actual) > 0, "リストが1つ以上取得できること")
