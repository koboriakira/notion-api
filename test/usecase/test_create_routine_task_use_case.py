from unittest import TestCase
from unittest.mock import Mock

from lotion.block import Divider
from notion_api.task.domain.routine_repository import RoutineRepository
from notion_api.task.domain.routine_task import RoutineTask, RoutineType
from notion_api.task.domain.task_repository import TaskRepository
from notion_api.usecase.create_routine_task_use_case import CreateRoutineTaskUseCase


class TestCreateRoutineTaskUseCase(TestCase):
    def setUp(self):
        mock_task_repository = Mock(spec=TaskRepository)
        mock_routine_repository = Mock(spec=RoutineRepository)
        routine_task = RoutineTask.create(title="ルーティンタスク", routine_type=RoutineType.DAILY)
        routine_task.block_children = [Divider()]
        mock_routine_repository.fetch_all.return_value = [routine_task]
        mock_task_repository.search.return_value = []
        self.suite = CreateRoutineTaskUseCase(
            task_repository=mock_task_repository, routine_repository=mock_routine_repository
        )
