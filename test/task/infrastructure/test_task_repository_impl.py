from datetime import date, datetime
from unittest import TestCase
from unittest.mock import Mock

from notion_api.domain.database_type import DatabaseType
from notion_api.domain.task.task import Task
from notion_api.domain.task.task_kind import TaskKindType
from notion_api.domain.task.task_status import TaskStatusType
from notion_api.infrastructure.task.task_repository_impl import TaskRepositoryImpl
from notion_api.notion_client_wrapper.client_wrapper import ClientWrapper
from notion_api.util.datetime import JST


class TestTaskRepositoryImpl(TestCase):
    def setUp(self) -> None:
        mock_client = Mock(spec=ClientWrapper)
        self.suite = TaskRepositoryImpl(notion_client_wrapper=mock_client)
        return super().setUp()

    def test_search_パラメータを利用できる(self):
        # Given
        status_list = [TaskStatusType.TODO, TaskStatusType.IN_PROGRESS]
        task_kind_type_list = [TaskKindType.NEXT_ACTION]
        start_datetime = datetime(2024, 1, 2, 12, 0, tzinfo=JST)
        start_datetime_end = datetime(2024, 1, 2, 13, 0, tzinfo=JST)

        # When
        _ = self.suite.search(
            status_list=status_list,
            kind_type_list=task_kind_type_list,
            start_datetime=start_datetime,
            start_datetime_end=start_datetime_end,
        )

        # Then
        self._assert_retrieve_page_called_once_with(
            filter_param={
                "and": [
                    {"property": "タスク種別", "select": {"does_not_equal": "ゴミ箱"}},
                    {"property": "実施日", "date": {"on_or_after": "2024-01-02T12:00:00+09:00"}},
                    {"property": "実施日", "date": {"on_or_before": "2024-01-02T13:00:00+09:00"}},
                    {"or": [{"property": "タスク種別", "select": {"equals": "次にとるべき行動リスト"}}]},
                    {
                        "or": [
                            {"property": "ステータス", "status": {"equals": "ToDo"}},
                            {"property": "ステータス", "status": {"equals": "InProgress"}},
                        ]
                    },
                ]
            },
        )

    def test_search_日付でも検索可能(self):
        # Given
        status_list = [TaskStatusType.TODO, TaskStatusType.IN_PROGRESS]
        task_kind_type_list = [TaskKindType.NEXT_ACTION]
        start_datetime = date(2024, 1, 2)
        start_datetime_end = date(2024, 1, 2)

        # When
        _ = self.suite.search(
            status_list=status_list,
            kind_type_list=task_kind_type_list,
            start_datetime=start_datetime,
            start_datetime_end=start_datetime_end,
        )

        # Then
        self._assert_retrieve_page_called_once_with(
            filter_param={
                "and": [
                    {"property": "タスク種別", "select": {"does_not_equal": "ゴミ箱"}},
                    {"property": "実施日", "date": {"on_or_after": "2024-01-02T00:00:00+09:00"}},
                    {"property": "実施日", "date": {"on_or_before": "2024-01-02T23:59:59.999999+09:00"}},
                    {"or": [{"property": "タスク種別", "select": {"equals": "次にとるべき行動リスト"}}]},
                    {
                        "or": [
                            {"property": "ステータス", "status": {"equals": "ToDo"}},
                            {"property": "ステータス", "status": {"equals": "InProgress"}},
                        ]
                    },
                ]
            },
        )

    def test_タスクを保存する(self):
        # Given
        task = Task.create(
            title="title",
        )
        self.suite.client.create_page_in_database.return_value = {"id": "dummy-id"}

        # When
        _ = self.suite.save(task=task)

        # Then
        self.suite.client.create_page_in_database.assert_called_once()
        self.suite.client.retrieve_page.assert_called_once()

    def _assert_retrieve_page_called_once_with(self, filter_param: dict):
        # Then
        # クラス名の一致をチェックするロジックがあるので、完全に合わせておく
        import sys

        sys.path.append("notion_api")
        from domain.task.task import Task as TaskModel

        self.suite.client.retrieve_database.assert_called_once_with(
            database_id=DatabaseType.TASK.value,
            filter_param=filter_param,
            page_model=TaskModel,
        )
