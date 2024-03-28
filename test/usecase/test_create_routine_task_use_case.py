

from unittest import TestCase
from unittest.mock import Mock

from notion_api.domain.task.routine_task import RoutineTask, RoutineType
from notion_api.domain.task.task import Task
from notion_api.domain.task.task_kind import TaskKindType
from notion_api.domain.task.task_repository import TaskRepository
from notion_api.infrastructure.task.routine_repository_impl import RoutineRepositoryImpl
from notion_api.notion_client_wrapper.block.divider import Divider
from notion_api.usecase.create_routine_task_use_case import CreateRoutineTaskUseCase
from notion_api.util.datetime import jst_today_datetime


class TestCreateRoutineTaskUseCase(TestCase):
    def setUp(self):
        mock_task_repository = Mock(spec=TaskRepository)
        mock_routine_repository = Mock(spec=RoutineRepositoryImpl)
        routine_task = RoutineTask.create(title="ルーティンタスク", routine_type=RoutineType.DAILY)
        routine_task.block_children = [Divider()]
        mock_routine_repository.fetch_all.return_value = [routine_task]
        mock_task_repository.search.return_value = []
        self.suite = CreateRoutineTaskUseCase(
            task_repository=mock_task_repository,
            routine_repository=mock_routine_repository
        )

    def test(self):
        # When
        self.suite.execute()

        # Then
        expected_task = Task.create(
            title="ルーティンタスク",
            task_kind_type=TaskKindType.SCHEDULE,
            start_date=jst_today_datetime(),
            blocks=[Divider()]
        )
        # self.suite.task_repository.save.assert_called_once_with(task=expected_task)
