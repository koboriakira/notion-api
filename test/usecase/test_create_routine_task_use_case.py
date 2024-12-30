from unittest import TestCase
from unittest.mock import Mock

from lotion import Lotion
from lotion.block import Divider
from notion_databases.routine_task import RoutineTask
from task.task_repository import TaskRepository
from notion_api.usecase.create_routine_task_use_case import CreateRoutineTaskUseCase


class TestCreateRoutineTaskUseCase(TestCase):
    def setUp(self):
        mock_task_repository = Mock(spec=TaskRepository)
        mock_lotion = Mock(spec=Lotion)
        routine_task = RoutineTask.generate(title="ルーティンタスク")
        routine_task.block_children = [Divider()]
        mock_lotion.retrieve_pages.return_value = [routine_task]
        mock_task_repository.search.return_value = []
        self.suite = CreateRoutineTaskUseCase(task_repository=mock_task_repository, lotion=mock_lotion)
