from unittest import TestCase
from unittest.mock import Mock

import pytest
from notion_api.domain.task.task import Task
from notion_api.infrastructure.task.task_repository_impl import TaskRepositoryImpl
from notion_api.notion_client_wrapper.client_wrapper import ClientWrapper


class TestTaskRepositoryImpl(TestCase):
    def setUp(self):
        self.genuine_client = ClientWrapper.get_instance()
        mock_client = Mock(spec=ClientWrapper)
        self.suite = TaskRepositoryImpl(notion_client_wrapper=mock_client)

    @pytest.mark.slow()
    def test_タスクを保存する(self):
        # Given
        task = Task.create(title="title",)
        self.suite.client.create_page_in_database.return_value = {"id": "dummy-id"}

        # When
        _ = self.suite.save(task=task)

        # Then
        self.suite.client.create_page_in_database.assert_called_once()
        self.suite.client.retrieve_page.assert_called_once()
