from unittest import TestCase

import pytest
from notion_api.usecase.fetch_tasks_usecase import FetchTasksUsecase


class TestFetchTasksUsecase(TestCase):
    def setUp(self):
        self.suite = FetchTasksUsecase()

    @pytest.mark.learning()
    def test_find_page(self):
        pass
