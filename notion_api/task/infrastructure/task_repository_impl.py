from datetime import date, datetime, time

from common.value.database_type import DatabaseType
from notion_client_wrapper.client_wrapper import ClientWrapper
from notion_client_wrapper.filter.condition.date_condition import DateCondition
from notion_client_wrapper.filter.condition.empty_condition import EmptyCondition
from notion_client_wrapper.filter.condition.or_condition import OrCondition
from notion_client_wrapper.filter.condition.relation_condition import RelationCondition
from notion_client_wrapper.filter.condition.string_condition import StringCondition
from notion_client_wrapper.filter.filter_builder import FilterBuilder
from notion_client_wrapper.page.page_id import PageId
from task.domain.project_relation import ProjectRelation
from task.domain.task import Task
from task.domain.task_kind import TaskKind, TaskKindType
from task.domain.task_repository import TaskRepository
from task.domain.task_start_date import TaskStartDate
from task.domain.task_status import TaskStatus, TaskStatusType
from util.datetime import JST


class TaskRepositoryImpl(TaskRepository):
    def __init__(self, notion_client_wrapper: ClientWrapper | None = None) -> None:
        self.client = notion_client_wrapper or ClientWrapper.get_instance()

    def search(  # noqa: PLR0913
        self,
        status_list: list[str | TaskStatusType] | None = None,
        kind_type_list: list[TaskKindType] | None = None,
        start_datetime: date | datetime | None = None,
        start_datetime_end: date | datetime | None = None,
        project_id: PageId | None = None,
    ) -> list[Task]:
        task_kind_trash = TaskKind.trash()
        filter_builder = FilterBuilder()
        filter_builder = filter_builder.add_condition(StringCondition.not_equal(property=task_kind_trash))
        if start_datetime is not None:
            start_datetime = (
                start_datetime
                if isinstance(start_datetime, datetime)
                else datetime.combine(start_datetime, time.min, tzinfo=JST)
            )
            task_start_date_after = TaskStartDate.create(start_datetime)
            filter_builder = filter_builder.add_condition(DateCondition.on_or_after(property=task_start_date_after))

        if start_datetime_end is not None:
            start_datetime_end = (
                start_datetime_end
                if isinstance(start_datetime_end, datetime)
                else datetime.combine(start_datetime_end, time.max, tzinfo=JST)
            )
            task_start_date_before = TaskStartDate.create(start_datetime_end)
            filter_builder = filter_builder.add_condition(DateCondition.on_or_before(property=task_start_date_before))

        if kind_type_list is not None:
            if len(kind_type_list) > 0:
                task_kind_properties = [TaskKind.create(kind_type=kind_type) for kind_type in kind_type_list]
                task_kind_equal_conditions = [
                    StringCondition.equal(property=task_kind) for task_kind in task_kind_properties
                ]
                or_condition = OrCondition(task_kind_equal_conditions)
                filter_builder = filter_builder.add_condition(or_condition)
            if len(kind_type_list) == 0:
                filter_builder = filter_builder.add_condition(EmptyCondition.true(TaskKind.NAME, TaskKind.TYPE))

        if status_list is not None and len(status_list) > 0:
            if isinstance(status_list[0], str):
                status_list = TaskStatusType.get_status_list(status_list)
            task_status_list = [TaskStatus.from_status_type(status_type) for status_type in status_list]
            task_status_equal_conditon = [
                StringCondition.equal(property=task_status) for task_status in task_status_list
            ]
            or_condition = OrCondition(task_status_equal_conditon)
            filter_builder = filter_builder.add_condition(or_condition)

        if project_id is not None:
            project_relation = ProjectRelation.from_id_list(id_list=[project_id.value])
            filter_builder = filter_builder.add_condition(RelationCondition.contains(project_relation))

        return self.client.retrieve_database(
            database_id=DatabaseType.TASK.value,
            filter_param=filter_builder.build(),
            page_model=Task,
        )

    def save(self, task: Task) -> Task:
        if task.id is not None:
            _ = self.client.update_page(page_id=task.id, properties=task.properties.values)
            return task
        page = self.client.create_page_in_database(
            database_id=DatabaseType.TASK.value,
            properties=task.properties.values,
            blocks=task.block_children,
        )
        return self.client.retrieve_page(page_id=page["id"], page_model=Task)

    def find_by_id(self, task_id: str) -> Task:
        return self.client.retrieve_page(page_id=task_id, page_model=Task)

    def move_to_backup(self, task: Task) -> None:
        # バックアップ用のデータベースにレコードを作成
        # タイトル、ステータス、実施日、タグ、プロジェクト、中身のみを移行
        properties = [
            task.get_title(),
        ]
        if task.get_date("実施日").start is not None:
            properties.append(task.get_date("実施日"))
        if task.get_relation("タグ") is not None:
            properties.append(task.get_relation("タグ"))
        if task.get_relation("プロジェクト") is not None:
            properties.append(task.get_relation("プロジェクト"))

        self.client.create_page_in_database(
            database_id=DatabaseType.TASK_BK.value,
            properties=properties,
            blocks=task.block_children,
        )

        # タスクを削除
        self.client.remove_page(page_id=task.id)
