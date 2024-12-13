from logging import Logger
from unittest import TestCase
from unittest.mock import Mock

import pytest
from notion_api.notion_client_wrapper.client_wrapper import Lotion
from notion_api.zettlekasten.infrastructure.zettlekasten_repository_impl import ZettlekastenRepositoryImpl


class TestZettlekastenRepositoryImpl(TestCase):
    def setUp(self) -> None:
        self.suite = ZettlekastenRepositoryImpl(
            client=Lotion.get_instance(),
            logger=Mock(spec=Logger),
        )
        return super().setUp()

    @pytest.mark.use_genuine_api()
    def test_searchが実行できる(self):
        zettlekastens = self.suite.search(is_tag_empty=True)
        self.assertIsNotNone(zettlekastens)
