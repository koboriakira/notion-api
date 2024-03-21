from unittest import TestCase
from unittest.mock import Mock

import pytest
from notion_api.domain.task.task_repository import TaskRepository
from notion_api.usecase.fetch_tasks_usecase import FetchTasksUsecase


class TestFetchTasksUsecase(TestCase):
    def setUp(self):
        mock_task_repository = Mock(spec=TaskRepository)
        self.suite = FetchTasksUsecase(task_repository=mock_task_repository)

    @pytest.mark.learning()
    def test_find_page(self):
        pass
