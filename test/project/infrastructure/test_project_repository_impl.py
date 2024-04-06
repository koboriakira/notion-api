from logging import Logger
from unittest import TestCase
from unittest.mock import Mock

import pytest
from notion_api.notion_client_wrapper.client_wrapper import ClientWrapper
from notion_api.project.infrastructure.project_repository_impl import ProjectRepositoryImpl


class Test(TestCase):
    def setUp(self) -> None:
        self.suite = ProjectRepositoryImpl(client=Mock(spec=ClientWrapper), logger=Mock(spec=Logger))
        return super().setUp()

    @pytest.mark.use_genuine_api()
    def test_fetch_all(self):
        # Given
        # When
        # 実際にNotion APIを叩くため、モックではなく本物のClientWrapperを使う
        suite = ProjectRepositoryImpl(client=ClientWrapper.get_instance(), logger=Mock(spec=Logger))
        projects = suite.fetch_all()

        # Then
        self.assertIsNotNone(projects)
        self.assertTrue(len(projects) > 0)
