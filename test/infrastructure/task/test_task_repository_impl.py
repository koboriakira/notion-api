from unittest import TestCase
from unittest.mock import Mock

import pytest
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
        task_id = "72452045863d42b8a5f1fd658dad8067" # https://www.notion.so/koboriakira/test-72452045863d42b8a5f1fd658dad8067?pvs=4
        task = self.genuine_client.retrieve_page(page_id=task_id)

        # When
        _ = self.suite.save(task=task)

        # Then
        self.fail()
